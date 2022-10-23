select distinct agc.condition_group_id as group_id, acg.achi_condition_group_name
     as group_name
from achi_generate_conditions as agc
left join achi_condition_groups as acg
     on agc.condition_group_id = acg.achi_condition_group_id
order by agc.condition_group_id;

select agc.condition_group_id as group_id, acg.achi_condition_group_name
     as group_name, agc.aggregate_id, agc.aggregate_name, agc.parameter_id,
     agc.parameter_name, agc.service_id, es.service_name
from achi_generate_conditions as agc
left join achi_condition_groups as acg
     on agc.condition_group_id = acg.achi_condition_group_id
left join external_services as es on agc.service_id = es.service_id;

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

select a.achievement_id, a.name
from achievements as a
right join (select unnest(achievements_id) as achievements_id
    from users_information where user_id = 0) as u
    on u.achievements_id = a.achievement_id;

select a.achievement_id, a.name
from achievements as a
right join
(
    select unnest(achievements_desired_id) as achievements_desired_id
    from users_information
    where user_id = 0
) as u on u.achievements_desired_id = a.achievement_id;

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
    select unnest({parameter}) as {parameter}
    from users_information
    where user_id = {user_id}
) as u
on u.{parameter} = a.achievement_id
left join approve_achievements as aa
    on aa.achievement_id = a.achievement_id
    and aa.user_passive_id = {user_id}
right join achi_conditions as ac on ac.condition_id = any(a.conditions)
right join achi_generate_conditions as agc
    on agc.parameter_id = ac.parameter_id and agc.condition_group_id = 7
where a.achievement_id is not null
group by a.achievement_id, a.name, ac.value;

select case when count(aa.user_active_id) > 0
    then true else false end as approved
from achievements as a
right join
(
    select unnest({parameter}) as {parameter}
    from users_information
    where user_id = {user_id}
) as u
on u.{parameter} = a.achievement_id
left join approve_achievements as aa
    on aa.achievement_id = a.achievement_id and
    aa.user_active_id = {user_active_id}
right join achi_conditions as ac on ac.condition_id = any(a.conditions)
right join achi_generate_conditions as agc
    on agc.parameter_id = ac.parameter_id and agc.condition_group_id = 7
where a.achievement_id is not null
group by a.achievement_id;

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