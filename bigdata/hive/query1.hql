use eignatenkov;

select * from parsed_text_log a
where a.status=200 and a.ip in (select min(ip) from parsed_text_log)
order by date
limit 1;

