import numpy as np
from scipy.stats import norm
from collections import Counter

def get_lpx_d_all(X, F, B, s):
    ##################################################################
    #
    # Calculates log(p(X_k|d_k,F,B,s)) for all images X_k in X and 
    # all possible displacements d_k.
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   F ... h x w numpy.array, estimate of villain's face
    #   B ... H x W numpy.array, estimate of background
    #   s ... 1 x 1, estimate of standart deviation of Gaussian noise
    #
    # Output parameters:
    #   
    #   lpx_d_all ... (H-h+1) x (W-w+1) x N numpy.array, 
    #                 lpx_d_all[dh,dw,k] - log-likelihood of 
    #                 observing image X_k given that the villain's 
    #                 face F is located at displacement (dh, dw)
    #
    ##################################################################
    bg_probs_precomp = norm.pdf(X, loc=np.expand_dims(B, axis=2), scale=s)
    result = np.zeros((X.shape[0] - F.shape[0] + 1, X.shape[1] - F.shape[1] + 1, X.shape[2]))
    f_x, f_y = F.shape
    face_3d = np.expand_dims(F, axis=2)
    for i in np.arange(X.shape[0] - F.shape[0] + 1):
        for j in np.arange(X.shape[1] - F.shape[1] + 1):
            bg_prob = bg_probs_precomp.copy()
            bg_prob[i:i+f_x, j:j+f_y, :] = norm.pdf(X[i:i+f_x, j:j+f_y, :], loc=face_3d, scale=s)
            result[i,j,:] = np.sum(np.nan_to_num(np.log(bg_prob)), axis=(0,1))
    return np.nan_to_num(result)

        
def calc_L(X, F, B, s, A, q, useMAP = False):
    ###################################################################
    #
    # Calculates the lower bound L(q,F,B,s,A) for the marginal log 
    # likelihood
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   F ... h x w numpy.array, estimate of villain's face
    #   B ... H x W numpy.array, estimate of background
    #   s ... 1 x 1, estimate of standart deviation of Gaussian noise
    #   A ... (H-h+1) x (W-w+1) numpy.array, estimate of prior on 
    #         displacement of face in any image
    #   q  ... if useMAP = False:
    #             (H-h+1) x (W-w+1) x N numpy.array, 
    #             q[dh,dw,k] - estimate of posterior of displacement 
    #             (dh,dw) of villain's face given image Xk
    #           if useMAP = True:
    #             2 x N numpy.array, 
    #             q[0,k] - MAP estimates of dh for X_k 
    #             q[1,k] - MAP estimates of dw for X_k 
    #   useMAP ... logical, if true then q is a MAP estimates of 
    #              displacement (dh,dw) of villain's face given image 
    #              Xk 
    #
    # Output parameters:
    #   
    #   L ... 1 x 1, the lower bound L(q,F,B,s,A) for the marginal log 
    #         likelihood
    #
    ###################################################################
    if useMAP:
        result = 0
        f_x, f_y = F.shape
        def get_lpxk_d(i, j, k):
            bg_prob = norm.pdf(X[:,:,k], loc=B, scale=s)
            bg_prob[i:i+f_x, j:j+f_y] = norm.pdf(X[i:i+f_x, j:j+f_y, k], loc=F, scale=s)
            return np.sum(np.nan_to_num(np.log(bg_prob)))
        for k in np.arange(q.shape[1]):
            i, j = q[:, k]
            result += get_lpxk_d(i, j, k)
            result += np.log(A[i,j])
        return result
    else:
        lpxd_all = np.nan_to_num(get_lpx_d_all(X, F, B, s) + np.expand_dims(np.nan_to_num(np.log(A)), 2))
        return np.sum(q * lpxd_all) - np.sum(q * np.nan_to_num(np.log(q)))
                
def e_step(X, F, B, s, A, useMAP = False):
    ##################################################################
    #
    # Given the current esitmate of the parameters, for each image Xk
    # esitmates the probability p(d_k|X_k,F,B,s,A)
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   F ... h x w numpy.array, estimate of villain's face
    #   B ... H x W numpy.array, estimate of background
    #   s ... 1 x 1, estimate of standart deviation of Gaussian noise
    #   A ... (H-h+1) x (W-w+1) numpy.array, estimate of prior on 
    #         displacement of face in any image
    #   useMAP ... logical, if true then q is a MAP estimates of 
    #              displacement (dh,dw) of villain's face given image 
    #              Xk 
    #
    # Output parameters:
    #   
    #   q  ... if useMAP = False:
    #             (H-h+1) x (W-w+1) x N numpy.array, 
    #             q[dh,dw,k] - estimate of posterior of displacement 
    #             (dh,dw) of villain's face given image Xk
    #           if useMAP = True:
    #             2 x N numpy.array, 
    #             q[0,k] - MAP estimates of dh for X_k 
    #             q[1,k] - MAP estimates of dw for X_k 
    ###################################################################
    lpx_d_all = get_lpx_d_all(X, F, B, s)
    max_logs = np.apply_over_axes(np.max, lpx_d_all, axes=(0,1))
    lpx_d_all_normed = lpx_d_all - max_logs
    A_3d = np.expand_dims(A, axis=2)
    pd_x_all_unnormed = np.nan_to_num(np.exp(lpx_d_all_normed))*A_3d
    normalizers = np.apply_over_axes(np.sum, pd_x_all_unnormed, axes=(0,1))
    pd_x_all = pd_x_all_unnormed/normalizers
    if not useMAP:
        return pd_x_all
    else:
        return np.column_stack(np.unravel_index(np.argmax(pd_x_all[:,:,i]), pd_x_all.shape[:2]) 
                               for i in np.arange(pd_x_all.shape[2]))

                        
def m_step(X, q, h, w, useMAP = False):
    ###################################################################
    # 
    # Estimates F,B,s,A given esitmate of posteriors defined by q
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   q ... if useMAP = False:
    #             (H-h+1) x (W-w+1) x N numpy.array, 
    #             q[dh,dw,k] - estimate of posterior of displacement 
    #             (dh,dw) of villain's face given image Xk
    #           if useMAP = True:
    #             2 x N numpy.array, 
    #             q[0,k] - MAP estimates of dh for X_k 
    #             q[1,k] - MAP estimates of dw for X_k 
    #   h ... 1 x 1, face mask hight
    #   w ... 1 x 1, face mask widht
    #  useMAP ... logical, if true then q is a MAP estimates of 
    #             displacement (dh,dw) of villain's face given image 
    #             Xk 
    #
    # Output parameters:
    #   
    #   F ... h x w numpy.array, estimate of villain's face
    #   B ... H x W numpy.array, estimate of background
    #   s ... 1 x 1, estimate of standart deviation of Gaussian noise
    #   A ... (H-h+1) x (W-w+1) numpy.array, estimate of prior on 
    #         displacement of face in any image
    ###################################################################
    H, W, N = X.shape
    if useMAP:
        q_counter = Counter()
        for i in range(N):
            q_counter[tuple(q[:,i])] += 1
        A = np.zeros((H-h+1, W-w+1))
        for key, value in q_counter.iteritems():
            A[key[0], key[1]] = value
        A = A/N
        F = np.zeros((h,w))
        for k in range(N):
            F += X[q[0,k]:q[0,k]+h, q[1,k]:q[1,k]+w, k]
        F = F/N
        B = np.zeros((H,W))
        for l in range(H):
            for m in range(W):
                pic_bool_index = np.ones(N).astype('bool')
                for k in range(N):
                    if q[0,k] <= l < q[0,k] + h and q[1,k] <= m < q[1,k] + w:
                        pic_bool_index[k] = False
                if np.sum(pic_bool_index) != 0:
                    B[l,m] = np.sum(X[l,m, pic_bool_index]).astype('float')/np.sum(pic_bool_index)
        v = np.zeros(N)
        for k in range(N):
            pic = B.copy()
            pic[q[0,k]:q[0,k]+h, q[1,k]:q[1,k]+w] = F
            v[k] = np.sum(np.square(X[:,:,k] - pic))
        s = np.sqrt(np.sum(v)/(H*W*N))
    else:
        A = np.apply_along_axis(np.sum, 2, q)/N
        F = np.zeros((h,w))
        for l in range(h):
            for m in range(w):
                F[l,m] = np.sum(X[l:l+q.shape[0],m:m+q.shape[1],:]*q)
        F = F/N
        B = np.zeros((H,W))
        for l in range(H):
            for m in range(W):
                q_copy = q.copy()
                for i in range(q_copy.shape[0]):
                    for j in range(q_copy.shape[1]):
                        if i <= l < i + h and j <= m < j + w:
                            q_copy[i,j,:] = 0
                if np.sum(q_copy) != 0:
                    B[l,m] = np.sum(X[l,m,:]*np.apply_over_axes(np.sum, q_copy, axes=(0,1)))/np.sum(q_copy)
        v = np.zeros(q.shape)
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                pic = B.copy()
                pic[i:i+h, j:j+w] = F
                v[i,j,:] = np.apply_over_axes(np.sum, np.square(X - np.expand_dims(pic, axis = 2)), axes=(0,1))
        s = np.sqrt(np.sum(q*v)/(H*W*N))
    return F, B, s, A

                                
def run_EM(X, h, w, F=None, B = None, s = None, A = None,
            tolerance = 0.001, max_iter = 50, useMAP = False):
    ###################################################################
    # 
    # Runs EM loop until the likelihood of observing X given current
    # estimate of parameters is idempotent as defined by a fixed 
    # tolerance
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   h ... 1 x 1, face mask hight
    #   w ... 1 x 1, face mask widht
    #   F, B, s, A ... initial parameters (optional!)
    #   F ... h x w numpy.array, estimate of villain's face
    #   B ... H x W numpy.array, estimate of background
    #   s ... 1 x 1, estimate of standart deviation of Gaussian noise
    #   A ... (H-h+1) x (W-w+1) numpy.array, estimate of prior on 
    #         displacement of face in any image
    #   tolerance ... parameter for stopping criterion
    #   max_iter  ... maximum number of iterations
    #   useMAP ... logical, if true then after E-step we take only 
    #              MAP estimates of displacement (dh,dw) of villain's 
    #              face given image Xk 
    #    
    #
    # Output parameters:
    #   
    #   F, B, s, A ... trained parameters
    #   LL ... 1 x (number_of_iters + 2) numpy.array, L(q,F,B,s,A) 
    #          at initial guess, after each EM iteration and after 
    #          final estimate of posteriors;
    #          number_of_iters is actual number of iterations that was 
    #          done
    ###################################################################
    H, W, N = X.shape 
    if F is None:
        F = np.ones((h,w))*256
    if B is None:
        B = np.zeros((H, W))
    if s is None:
        s = 64
    if A is None:
        A = np.ones((H-h+1, W-w+1))/((H-h+1)*(W-w+1))
    if useMAP:
        q = np.zeros((2, N))
    else:
        q = np.repeat(A[:, :, np.newaxis], N, axis=2)
    LL = []
    LL.append(calc_L(X, F, B, s, A, q, useMAP))
    for i in range(max_iter):
        q = e_step(X, F, B, s, A, useMAP)
        F, B, s, A = m_step(X, q, h, w, useMAP)
        next_l = calc_L(X, F, B, s, A, q, useMAP)
        LL.append(next_l)
        if np.abs(LL[-2]-LL[-1]) < tolerance:
            break
    q = e_step(X, F, B, s, A, useMAP)
    LL.append(calc_L(X, F, B, s, A, q, useMAP))
    return F, B, s, A, LL


def run_EM_with_restarts(X, h, w, tolerance = 0.001, max_iter = 50,
                             useMAP = False, restart=10):
    ###################################################################
    # 
    # Restarts EM several times from different random initializations 
    # and stores the best estimate of the parameters as measured by 
    # the L(q,F,B,s,A)
    #
    # Input parameters:
    #
    #   X ... H x W x N numpy.array, N images of size H x W
    #   h ... 1 x 1, face mask hight
    #   w ... 1 x 1, face mask widht
    #   tolerance, max_iter, useMAP ... parameters for EM
    #   restart   ... number of EM runs
    #
    # Output parameters:
    #   
    #   F ... h x w numpy.array, the best estimate of villain's face
    #   B ... H x W numpy.array, the best estimate of background
    #   s ... 1 x 1, the best estimate of standart deviation of 
    #         Gaussian noise
    #   A ... (H-h+1) x (W-w+1) numpy.array, the best estimate of 
    #         prior on displacement of face in any image
    #   LL ... 1 x 1, the best L(q,F,B,s,A)
    ###################################################################
    H, W, N = X.shape
    F_list = []
    B_list = []
    s_list = []
    A_list = []
    LL_list = []
    
    for i in range(restart):
        F_start = np.random.randint(0, 256, (h, w))
        B_start = np.random.randint(0, 256, (H, W))
        s_start = np.random.randint(1, 256)
        A_start = np.random.rand(H-h+1, W-w+1)
        A_start = A_start/np.sum(A_start)
        F_next, B_next, s_next, A_next, LL_next = run_EM(X, h, w, F=F_start, B=B_start, 
                                                         s=s_start, A=A_start, tolerance=tolerance,
                                                         max_iter=max_iter, useMAP=useMAP)
        F_list.append(F_next)
        B_list.append(B_next)
        s_list.append(s_next)
        A_list.append(A_next)
        LL_list.append(LL_next[-1])
        print i, 'done'
    best_index = np.argmax(np.array(LL_list))
    return F_list[best_index], B_list[best_index], s_list[best_index], A_list[best_index], LL_list[best_index]

