CREATE TABLE public.task_status (
	id uuid NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT task_status_pk PRIMARY KEY (id)
);

INSERT INTO public.task_status
    (id, "name" )
VALUES
    ('a385655d-fc2e-4baa-9ac6-8ea1306383ff', 'pending'),
    ('ed8ce546-8866-4c2c-b294-9216d87a1cba', 'error'),
    ('30b991d6-fa99-4c16-814b-5ac9c6d131a5', 'success');

CREATE TABLE public."configuration" (
	id uuid NOT NULL,
	eq_id varchar NOT NULL,
	status uuid NOT NULL,
	CONSTRAINT configuration_pk PRIMARY KEY (id)
);

ALTER TABLE public."configuration" ADD CONSTRAINT configuration_task_status_fk FOREIGN KEY (status) REFERENCES public.task_status(id) ON DELETE CASCADE ON UPDATE CASCADE;