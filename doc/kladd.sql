-- Lister alle turer pr bruke
select id, tour_date
from tours
WHERE
user_id = 6
AND
tour_date >= '2021-01-01'
order by tour_date

-- Toppliste
select t.user_id, u.username, count(*) count_tours
from tours t
join users u on u.id = t.user_id
WHERE
t.tour_date >= '2021-01-01'
group by t.user_id
order by count(*) DESC

-- Siste turer
select t.*, u.username 
from tours t
join users u on u.id = t.user_id
order by t.tour_date desc, t.created desc
limit 10
