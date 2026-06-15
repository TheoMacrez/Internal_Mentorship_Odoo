

-- object: public.name_length | type: DOMAIN --
-- DROP DOMAIN IF EXISTS public.name_length CASCADE;
CREATE DOMAIN public.name_length AS varchar(50)
	CONSTRAINT length CHECK (length(btrim(VALUE)) >= 2);
-- ddl-end --
ALTER DOMAIN public.name_length OWNER TO postgres;
-- ddl-end --

-- object: public.skill | type: TABLE --
-- DROP TABLE IF EXISTS public.skill CASCADE;
CREATE TABLE public.skill (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name varchar(50) NOT NULL,
	skill_type varchar,
	CONSTRAINT pk_skill PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.skill OWNER TO postgres;
-- ddl-end --

-- object: public.employee_skill | type: TABLE --
-- DROP TABLE IF EXISTS public.employee_skill CASCADE;
CREATE TABLE public.employee_skill (
	level smallint,
	employee_id smallint NOT NULL,
	skill_id smallint NOT NULL

);
-- ddl-end --
ALTER TABLE public.employee_skill OWNER TO postgres;
-- ddl-end --

-- object: public.employee | type: TABLE --
-- DROP TABLE IF EXISTS public.employee CASCADE;
CREATE TABLE public.employee (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	first_name public.name_length NOT NULL,
	last_name varchar(50) NOT NULL,
	email varchar(50),
	phone varchar(50),
	birth_date date,
	CONSTRAINT pk_employee PRIMARY KEY (id),
	CONSTRAINT uq_employee_email UNIQUE (email),
	CONSTRAINT chk_empty_first_name CHECK (length(btrim(first_name)) <=2)
);
-- ddl-end --
ALTER TABLE public.employee OWNER TO postgres;
-- ddl-end --

-- object: public.mentor_profile | type: TABLE --
-- DROP TABLE IF EXISTS public.mentor_profile CASCADE;
CREATE TABLE public.mentor_profile (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	max_mentees integer GENERATED ALWAYS AS (1) STORED,
	employee_id smallint,
	CONSTRAINT pk_profile PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.mentor_profile OWNER TO postgres;
-- ddl-end --

-- object: public.availability | type: TABLE --
-- DROP TABLE IF EXISTS public.availability CASCADE;
CREATE TABLE public.availability (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	day_of_week varchar(20) NOT NULL,
	start_time time NOT NULL,
	end_time time NOT NULL,
	CONSTRAINT pk_availability PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.availability OWNER TO postgres;
-- ddl-end --

-- object: public.request | type: TABLE --
-- DROP TABLE IF EXISTS public.request CASCADE;
CREATE TABLE public.request (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	start_level smallint,
	target_level smallint,
	CONSTRAINT pk_request PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.request OWNER TO postgres;
-- ddl-end --

-- object: public.mentorship | type: TABLE --
-- DROP TABLE IF EXISTS public.mentorship CASCADE;
CREATE TABLE public.mentorship (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	start_date date NOT NULL,
	end_date date NOT NULL,
	status varchar(50) NOT NULL,
	score smallint NOT NULL,
	CONSTRAINT pk_mentorship PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE public.mentorship OWNER TO postgres;
-- ddl-end --

-- object: fk_employee_skill_to_employee | type: CONSTRAINT --
-- ALTER TABLE public.employee_skill DROP CONSTRAINT IF EXISTS fk_employee_skill_to_employee CASCADE;
ALTER TABLE public.employee_skill ADD CONSTRAINT fk_employee_skill_to_employee FOREIGN KEY (employee_id)
REFERENCES public.employee (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_employee_skill_to_skill | type: CONSTRAINT --
-- ALTER TABLE public.employee_skill DROP CONSTRAINT IF EXISTS fk_employee_skill_to_skill CASCADE;
ALTER TABLE public.employee_skill ADD CONSTRAINT fk_employee_skill_to_skill FOREIGN KEY (skill_id)
REFERENCES public.skill (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_profile_to_employee | type: CONSTRAINT --
-- ALTER TABLE public.mentor_profile DROP CONSTRAINT IF EXISTS fk_profile_to_employee CASCADE;
ALTER TABLE public.mentor_profile ADD CONSTRAINT fk_profile_to_employee FOREIGN KEY (employee_id)
REFERENCES public.employee (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_availability_to_employee | type: CONSTRAINT --
-- ALTER TABLE public.availability DROP CONSTRAINT IF EXISTS fk_availability_to_employee CASCADE;
ALTER TABLE public.availability ADD CONSTRAINT fk_availability_to_employee FOREIGN KEY (id)
REFERENCES public.employee (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_request_to_employee | type: CONSTRAINT --
-- ALTER TABLE public.request DROP CONSTRAINT IF EXISTS fk_request_to_employee CASCADE;
ALTER TABLE public.request ADD CONSTRAINT fk_request_to_employee FOREIGN KEY (id)
REFERENCES public.employee (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_request_to_skill | type: CONSTRAINT --
-- ALTER TABLE public.request DROP CONSTRAINT IF EXISTS fk_request_to_skill CASCADE;
ALTER TABLE public.request ADD CONSTRAINT fk_request_to_skill FOREIGN KEY (id)
REFERENCES public.skill (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_mentorship_to_mentor | type: CONSTRAINT --
-- ALTER TABLE public.mentorship DROP CONSTRAINT IF EXISTS fk_mentorship_to_mentor CASCADE;
ALTER TABLE public.mentorship ADD CONSTRAINT fk_mentorship_to_mentor FOREIGN KEY (id)
REFERENCES public.mentor_profile (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_mentorship_to_mentee | type: CONSTRAINT --
-- ALTER TABLE public.mentorship DROP CONSTRAINT IF EXISTS fk_mentorship_to_mentee CASCADE;
ALTER TABLE public.mentorship ADD CONSTRAINT fk_mentorship_to_mentee FOREIGN KEY (id)
REFERENCES public.employee (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_mentorship_to_request | type: CONSTRAINT --
-- ALTER TABLE public.mentorship DROP CONSTRAINT IF EXISTS fk_mentorship_to_request CASCADE;
ALTER TABLE public.mentorship ADD CONSTRAINT fk_mentorship_to_request FOREIGN KEY (id)
REFERENCES public.request (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: fk_mentorship_to_skill | type: CONSTRAINT --
-- ALTER TABLE public.mentorship DROP CONSTRAINT IF EXISTS fk_mentorship_to_skill CASCADE;
ALTER TABLE public.mentorship ADD CONSTRAINT fk_mentorship_to_skill FOREIGN KEY (id)
REFERENCES public.skill (id) MATCH SIMPLE
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


