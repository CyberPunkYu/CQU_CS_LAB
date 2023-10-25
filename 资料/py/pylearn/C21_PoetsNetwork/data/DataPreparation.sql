-- SQLite

-- 死于唐朝建立前的人
-- delete from poet
-- where deathyear < 618 and deathyear !=0 and deathyear is not null;


-- 生成唐朝灭亡后的人
-- delete from poet
-- where birthyear > 907 and birthyear !=0 and birthyear is not null;

-- 生卒年全不详的人
-- delete from poet
-- where birthyear = 0 and deathyear = 0;

-- 唐灭亡80年后才死的人也不可能是唐朝人
-- delete from poet
-- where deathyear > 907 + 80;

-- 生年明确且于唐建立前80年生出的人也不可能是唐朝人
-- delete from poet
-- where birthyear > 0 and birthyear < 618 - 80;

-- 压缩多余数据库空间
-- VACUUM

-- 删除常用词别称
-- delete from altname where name like '%無作%';


-- create table reference 
-- (authorid int, refid int, poemid int);

-- create index idx_ref_author_ref on reference (authorid, refid);

-- select * from poet
-- where name like '%李%';
-- select * from poem;

SELECT authorid, refid, count(*) as cnt FROM reference
GROUP BY authorid, refid 
ORDER BY cnt DESC 
LIMIT 100;





















