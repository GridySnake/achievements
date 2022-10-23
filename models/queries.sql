--achievements!

--data_for_group_drop_down_generate_achievements (q1)
select distinct agc.condition_group_id as group_id, acg.achi_condition_group_name
     as group_name
from achi_generate_conditions as agc
left join achi_condition_groups as acg
     on agc.condition_group_id = acg.achi_condition_group_id
order by agc.condition_group_id;

--data_for_drop_downs_generate_achievements (q2)
select agc.condition_group_id as group_id, acg.achi_condition_group_name
     as group_name, agc.aggregate_id, agc.aggregate_name, agc.parameter_id,
     agc.parameter_name, agc.service_id, es.service_name
from achi_generate_conditions as agc
left join achi_condition_groups as acg
     on agc.condition_group_id = acg.achi_condition_group_id
left join external_services as es on agc.service_id = es.service_id;

--get_achievement_conditions (q3)
select agc.parameter_name, agc.condition_group_id, agc.aggregate_id,
      agc.service_id, ui.services_username, c.geo, c.value, c.equality,
          c.parameter_id, c.condition_id
from (select conditions from achievements where
      achievement_id = 1) as a
left join achi_conditions as c on c.condition_id = any(a.conditions)
left join achi_generate_conditions agc on c.parameter_id = agc.parameter_id
left join (select services_id, unnest(services_username) as services_username,
      unnest(services_id) as services_ids
      from users_information where user_id = 0) as ui
      on agc.service_id = ui.services_ids
order by agc.service_id;

--get_users_achievements (q4)
select a.achievement_id, a.name
from achievements as a
right join (select unnest(achievements_id) as achievements_id
    from users_information where user_id = 0) as u
    on u.achievements_id = a.achievement_id;

--get_users_desire_achievements (q5)
select a.achievement_id, a.name
from achievements as a
right join
(
    select unnest(achievements_desired_id) as achievements_desired_id
    from users_information
    where user_id = 0
) as u on u.achievements_desired_id = a.achievement_id;

--get_users_approve_achievements (q6)
select a.achievement_id, a.name,
    COUNT(aa.user_passive_id) as approve_count,
    ac.value::int as approve_need,
    round(COUNT(aa.user_passive_id)::numeric /
        ac.value::int * 100, 2)::varchar
        as current_percentage,
    round(1.0 / ac.value::int * 100, 2)::varchar as step_percentage,
    Extract(minute FROM statement_timestamp() - max(datetime))::int as delta
from achievements as a
right join
(
    select unnest(achievements_desired_id) as achievements_desired_id
    from users_information
    where user_id = 0
) as u
on u.achievements_desired_id = a.achievement_id
left join approve_achievements as aa
    on aa.achievement_id = a.achievement_id
    and aa.user_passive_id = 0
right join achi_conditions as ac on ac.condition_id = any(a.conditions)
right join achi_generate_conditions as agc
    on agc.parameter_id = ac.parameter_id and agc.condition_group_id = 7
where a.achievement_id is not null
group by a.achievement_id, a.name, ac.value;

--is_user_approved (q7)
select case when count(aa.user_active_id) > 0
    then true else false end as approved
from achievements as a
right join
(
    select unnest(achievements_desired_id) as achievements_desired_id
    from users_information
    where user_id = 0
) as u
on u.achievements_desired_id = a.achievement_id
left join approve_achievements as aa
    on aa.achievement_id = a.achievement_id and
    aa.user_active_id = 0
right join achi_conditions as ac on ac.condition_id = any(a.conditions)
right join achi_generate_conditions as agc
    on agc.parameter_id = ac.parameter_id and agc.condition_group_id = 7
where a.achievement_id is not null
group by a.achievement_id;

--get_achievement_info (q8)
select a.achievement_id:: varchar, a.name, a.description, agc.aggregate_name,
    c.parameter_id:: varchar, c.value,
    g.achi_condition_group_name, a.created_date::varchar, a.new, u.name as u_name,
    u.surname as u_surname, u.user_id, c.geo, c.condition_id, s.sphere_name,
    s.subsphere_name, c.test_url, g.achi_condition_group_id
from achi_conditions as c
right join (select achievement_id, unnest(conditions) as conditions, name,
    user_id, description, created_date, new, subsphere_id from achievements)
    as a on a.conditions::integer = c.condition_id
left join achi_generate_conditions as agc
    on c.parameter_id = agc.parameter_id
left join achi_condition_groups as g
    on g.achi_condition_group_id = agc.condition_group_id
left join users_information as u on a.user_id = u.user_id
left join spheres s on a.subsphere_id = s.subsphere_id
where a.achievement_id = 1;

--get_achievement_by_condition_id (q9)
select a.achievement_id, a.name, c.value, c.geo
from achi_conditions as c
left join (select achievement_id, name, unnest(conditions) as conditions from achievements) as a
    on a.conditions::integer = c.condition_id
where c.condition_id = 1;

--get_achievement_by_token (q10)
select a.achievement_id
from achievements as a
where a.achievement_qr = 'ejfhlifhasfjaskhfjmalfjldjhfajlsoi';

--get_achievement_by_condition_value (q11)
select a.achievement_id
from achi_conditions as c
left join (select achievement_id, conditions from achievements) as a
    on c.condition_id = any(a.conditions)
left join achi_generate_conditions agc on c.parameter_id = agc.parameter_id
where c.value = 'djdfjoahfhdsaivdhalfhahfij';

--get_achievement_by_condition_parameter (q12)
select a.achievement_id, a.name, c.value, c.geo, agc.condition_group_id
from achi_conditions as c
left join (select achievement_id, name, unnest(conditions) as conditions from achievements) as a
    on a.conditions::integer = c.condition_id
left join achi_generate_conditions agc on c.parameter_id = agc.parameter_id
where c.parameter_id = 'sfhalkfhak';

--get_created_achievements (q13)
select achievement_id, a.name, a.description, achievement_qr, s.sphere_name, s.subsphere_name, c.community_name,
    co.course_name
from achievements as a
left join spheres as s on a.subsphere_id = s.subsphere_id
left join communities as c on a.user_id = any(c.community_owner_id) and user_type = 1
left join courses as co on co.course_owner_id = a.user_id and user_type = 2
where (a.user_id = 0 and user_type = 0) or c.community_name is not null or co.course_name is not null
order by a.created_date desc;

--is_achievement_owner (q14)
select case when count(achievement_id) > 0 then true else false end
    as owner
from achievements as a
left join communities as c on a.user_id = any(c.community_owner_id)
    and user_type = 1
left join courses as co on co.course_owner_id = a.user_id
    and user_type = 2
where a.achievement_id = 1 and ((a.user_id = 0
    and user_type = 0) or c.community_name is not null or
        co.course_name is not null);

--get_reached_achievements (q15)
select achievement_id, a.name, a.description, s.sphere_name, s.subsphere_name, u.hide_achievements
from (select user_id, unnest(achievements_id) as achievements_id, unnest(hide_achievements) as hide_achievements from users_information) as u
inner join achievements as a on u.achievements_id = a.achievement_id
left join spheres s on a.subsphere_id = s.subsphere_id
where u.user_id = 0;

--get_suggestion_achievements (q16)
select achievement_id, a.user_id, a.user_type, a.name as title, a.description, a.created_date::varchar, a.new,
    u.name, u.surname, s.sphere_name, s.subsphere_name, c.community_name, c.community_owner_id,
    co.course_name
from achievements as a
left join users_information as u on u.user_id = a.user_id and a.user_type = 0
left join communities as c on a.user_id = c.community_id and a.user_type = 1
left join courses as co on co.course_id = a.user_id and a.user_type = 2
left join spheres s on a.subsphere_id = s.subsphere_id
left join users_information as u1 on a.achievement_id = any(u1.achievements_id)
    or a.achievement_id = any(u1.achievements_desired_id)
where (0 <> any(c.community_owner_id) or c.community_owner_id is null) and
      (0 <> co.course_owner_id or co.course_owner_id is null) and
      (u1.user_id is null or u1.user_id <> 0) and
      u.user_id <> 0;

--is_reach_achievement (q17)
select case when count(*) > 0 then true else false end as is_reached
from users_information
where user_id = 0 and 1 = any(achievements_id);

--is_drop (q18)
select
       case when count(ui.user_id) < 10 or extract(month from age(a.created_date)) < 1 then true
        else false
    end as is_drop
from achievements as a
left join users_information as ui on a.achievement_id = any(ui.achievements_id)
where a.achievement_id = 1
group by a.achievement_id;

--give_achievement_to_user (q19)
update users_information
set achievements_id = array_append(achievements_id, 1)
where user_id = 0 and 1 not in (
        select unnest(achievements_id) from users_information where user_id = 0);

--take_away_achievement (q20)
update users_information
set achievements_id = achievements_id[:(select
 array_position(ui.achievements_id,
 1) from users_information as ui where user_id = 0 and
 1 = any(achievements_id))-1] ||
 achievements_id[(select array_position(ui.achievements_id,
     1)
 from users_information as ui where user_id = user_id and 1 =
 any(achievements_id))+1:]
 where user_id = 0;

--qr_verify (q21)
select a.achievement_id
from achi_conditions as c
inner join (select achievement_id, unnest(conditions) as conditions, achievement_qr from
achievements) as a on a.conditions::integer = c.condition_id
left join achi_generate_conditions agc on c.parameter_id = agc.parameter_id
where agc.condition_group_id = 1 and a.achievement_qr = 'jgkhljkjfhdgsfafgdhf';

--show_achievement (q22)
update users_information
set hide_achievements = hide_achievements[:(select array_position(ui.achievements_id,
    1) from users_information as ui where user_id = 0)-1] ||
    array[0] ||
    hide_achievements[(select array_position(ui.achievements_id,
    0) from users_information as ui where user_id = 0)+1:]
where user_id = 0;

--hide_achievement (q23)
update users_information
set hide_achievements = hide_achievements[:(select array_position(ui.achievements_id,
    1) from users_information as ui where user_id = 0)-1] ||
    array[1] ||
    hide_achievements[(select array_position(ui.achievements_id,
    1) from users_information as ui where user_id = 0)+1:]
where user_id = 0;

--approve_verify (q24)
select case when a.achievement_id is null then false
        else true
        end as approve
from (select achievement_id, conditions from achievements
    where achievement_id = 1) as a
left join achi_conditions as c on c.condition_id = any(a.conditions)
    and c.parameter_id = 1
left join (
    select a.achievement_id, COUNT(aa.user_passive_id) as approve_count
from achievements as a
left join approve_achievements as aa
    on aa.achievement_id = a.achievement_id
    where aa.user_passive_id = 0
group by a.achievement_id) as q on q.achievement_id = a.achievement_id
where c.value::integer <= q.approve_count;

--desire_achievement (q25)
update users_information
set achievements_desired_id = array_append(achievements_desired_id, 1)
where user_id = 0
     and 1 not in (
select unnest(achievements_desired_id)
from users_information
where user_id = 0);

--undesire_achievement (q26)
update users_information
set achievements_desired_id = achievements_desired_id[:(select
 array_position(ui.achievements_desired_id,
 1) from users_information as ui where user_id = 0 and
 1 = any(achievements_desired_id))-1] ||
 achievements_desired_id[(select array_position(ui.achievements_desired_id,
     1)
 from users_information as ui where user_id = 0 and 1 =
 any(achievements_desired_id))+1:]
 where user_id = 0;

--is_desire (q27)
select count(achievements_desired_id)
from (select unnest(achievements_desired_id) as achievements_desired_id from users_information where user_id = 0) as u
where u.achievements_desired_id = 1;

--is_desire_achievement (q28)
select count(achievement_id) as count
from achievements as a
left join users_information as u on u.user_id = a.user_id and a.user_type = 0 and u.user_id <> 0
left join communities as c on a.user_id = c.community_id and a.user_type = 1
    and (0 <> any(c.community_owner_id) or c.community_owner_id is null)
left join courses as co on co.course_id = a.user_id and a.user_type = 2
    and (0 <> co.course_owner_id or co.course_owner_id is null)
left join users_information as u1 on a.achievement_id = any(u1.achievements_desired_id)
where u1.user_id = 0 and a.achievement_id = 1;

--approve_achievement (q29)
insert into approve_achievements (approvement_id, user_active_id, user_passive_id,
     achievement_id, datetime) values (
1, 1, 0, 1, statement_timestamp());

--disapprove_achievement (q30)
delete from approve_achievements
where user_passive_id = 1 and user_active_id = 0
    and achievement_id = 1;

--get_data_for_test (q31)
select c.answers_url
from achi_conditions as c
where c.condition_id=1;

--delete_achievement (q32)
update users_information
set achievements_id = achievements_id[:(select array_position(ui.achievements_id,
     1) from users_information as ui where 1 =
     any(achievements_id))-1] ||
     achievements_id[(select array_position(ui.achievements_id, 1)
     from users_information as ui where 1 = any(achievements_id))+1:],
achievements_desired_id = achievements_desired_id[:(select
     array_position(ui.achievements_desired_id,
     1) from users_information as ui where 1 =
     any(achievements_desired_id))-1] ||
     achievements_desired_id[(select array_position(ui.achievements_desired_id,
         1)
     from users_information as ui where 1 =
     any(achievements_desired_id))+1:];

--create_achievement (q33)
insert into achievements (achievement_id, user_id, user_type, name, description,
conditions, created_date, new, achievement_qr, sphere_id, subsphere_id) values(
1, 0, 0, 'sgdhjffj', 'fsgdhfjg',
ARRAY[1], statement_timestamp(), true, 'sghdjf',
1, 1);