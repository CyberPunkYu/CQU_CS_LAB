# 创建学生表，保存学号和密码
create table if not exists student(
    stu_num varchar(20) primary key ,
    stu_pass varchar(20)
);

# 创建学生信息表，保存学生的学籍信息，以学号为外键
create table if not exists message(
    stu_num varchar(20) primary key ,
    name varchar(10) ,
    gender char ,
    age int ,
    origin varchar(20) ,
    class char ,
    major varchar(20) ,
    image varchar(200) ,
    FOREIGN KEY(stu_num) REFERENCES student(stu_num)
);

CREATE TABLE IF NOT EXISTS geographic_and_time(
    stu_num varchar(20) primary key ,
    longitude DECIMAL(20,17) ,
    latitude DECIMAL(20,17) ,
    time DATE ,
    FOREIGN KEY(stu_num) REFERENCES student(stu_num)
);




# 创建填充student表的存储过程
DROP PROCEDURE add_stu;

DELIMITER //

CREATE PROCEDURE add_stu(INOUT number INT, IN times INT)
BEGIN
    DECLARE loop_count INT DEFAULT 0;
    label_loop:LOOP
        if loop_count >= times THEN LEAVE label_loop;
        END IF;

        INSERT INTO student VALUES (CONCAT('a', number), '123456');
        SET number = number + 1;
        SET loop_count = loop_count + 1;
    END LOOP label_loop;
END //

DELIMITER ;



DROP PROCEDURE board_info;
# 看板数据模拟
DELIMITER &

CREATE PROCEDURE board_info(INOUT number INT, IN times INT)
BEGIN
    DECLARE loop_count INT DEFAULT 0;
    DECLARE lastname CHAR;
    DECLARE firstname varchar(10);
    DECLARE gender CHAR;
    DECLARE age INT;
    DECLARE origin VARCHAR(20);
    DECLARE class int;
    DECLARE major VARCHAR(20);
    DECLARE lat DECIMAL(20,17);
    DECLARE lng DECIMAL(20,17);
    DECLARE time DATE;
    DECLARE random_num DOUBLE;
    label_loop:LOOP
        if loop_count >= times THEN LEAVE label_loop;
        END IF;

        SET random_num = RAND();

        IF random_num <= 0.5 THEN SET gender = '男';
        ELSE SET gender = '女';
        END IF;

        SET random_num = RAND();

        IF random_num < 0.2 THEN SET age = 16;
        ELSEIF random_num < 0.4 THEN SET age = 17;
        ELSEIF random_num < 0.6 THEN SET age = 18;
        ELSEIF random_num < 0.8 THEN SET age = 19;
        ELSE SET age = 20;
        END IF ;

        SET random_num = RAND();

        IF random_num < 0.5 THEN SET major = '大数据技术';
        ELSEIF random_num < 0.8 THEN SET major = '云计算技术应用';
        ELSE SET major = '物联网应用技术';
        END IF ;

        SET random_num = RAND();

        CASE
            WHEN random_num <= 0.01 THEN SET origin = '遵义市' , lat = 28.14 , lng = 107.08;
            WHEN random_num <= 0.04 THEN SET origin = '毕节市' , lat = 27.10 , lng = 105.26;
            WHEN random_num <= 0.09 THEN SET origin = '贵阳市' , lat = 26.78 , lng = 106.71;
            WHEN random_num <= 0.16 THEN SET origin = '六盘水市' , lat = 26.10 , lng = 104.80;
            WHEN random_num <= 0.25 THEN SET origin = '安顺市' , lat = 26.05 , lng = 105.92;
            WHEN random_num <= 0.36 THEN SET origin = '铜仁市' , lat = 27.99 , lng = 108.56;
            WHEN random_num <= 0.49 THEN SET origin = '黔西南布依族苗族自治州' , lat = 25.30 , lng = 105.52;
            WHEN random_num <= 0.64 THEN SET origin = '黔南布依族苗族自治州' , lat = 26.00 , lng = 107.22;
            WHEN random_num <= 0.81 THEN SET origin = '黔东南苗族侗族自治州' , lat = 26.50 , lng = 108.62;
            WHEN random_num <= 1 THEN SET origin = '贵州省外';
        END CASE ;

        SET random_num = RAND();

        IF random_num <= 0.5 THEN SET time = DATE_SUB(now(), INTERVAL 1 DAY);
        ELSE SET time = now();
        END IF;

        SET random_num = RAND();

        IF random_num <= 0.3 THEN SET class = '1';
        ELSEIF random_num <= 0.3 THEN SET class = '2';
        ELSE SET class = '3';
        END IF;

        SET random_num = RAND();

        CASE
            WHEN random_num <= 0.01 THEN SET lastname = '安';
            WHEN random_num <= 0.04 THEN SET lastname = '黎';
            WHEN random_num <= 0.09 THEN SET lastname = '蒋';
            WHEN random_num <= 0.16 THEN SET lastname = '刘';
            WHEN random_num <= 0.25 THEN SET lastname = '曾';
            WHEN random_num <= 0.36 THEN SET lastname = '陈';
            WHEN random_num <= 0.49 THEN SET lastname = '邓';
            WHEN random_num <= 0.64 THEN SET lastname = '王';
            WHEN random_num <= 0.81 THEN SET lastname = '徐';
            WHEN random_num <= 1 THEN SET lastname = '张';
            END CASE ;

        SET random_num = RAND();

        CASE
            WHEN random_num <= 0.01 THEN SET firstname = '伟';
            WHEN random_num <= 0.04 THEN SET firstname = '伟杰';
            WHEN random_num <= 0.09 THEN SET firstname = '胜';
            WHEN random_num <= 0.16 THEN SET firstname = '秦';
            WHEN random_num <= 0.25 THEN SET firstname = '昊';
            WHEN random_num <= 0.36 THEN SET firstname = '昊天';
            WHEN random_num <= 0.49 THEN SET firstname = '胜利';
            WHEN random_num <= 0.64 THEN SET firstname = '建军';
            WHEN random_num <= 0.81 THEN SET firstname = '俊豪';
            WHEN random_num <= 1 THEN SET firstname = '俊杰';
            END CASE ;


        INSERT INTO student VALUES (CONCAT('a', number), '123456');
        INSERT INTO message VALUES (CONCAT('a', number), CONCAT(lastname,firstname), gender, age, origin, class, major, 'http://rgnlwzaux.hn-bkt.clouddn.com/20204000.jpeg');
        IF origin = '贵州省外' THEN INSERT INTO geographic_and_time(stu_num, time) VALUES (CONCAT('a', number), time);
        ELSE INSERT INTO geographic_and_time VALUES (CONCAT('a', number), lng, lat, time);
        END IF;

        SET number = number + 1;
        SET loop_count = loop_count + 1;
    END LOOP label_loop;
END &

DELIMITER ;

SET @number = 20220000;
SET @times = 500;
CALL board_info(@number, @times);

SET @number = 20220500;
SET @times = 500;
CALL add_stu(@number, @times);

TRUNCATE TABLE geographic_and_time;
DELETE FROM student where stu_num >= 0;


