create table banks
(
    id    serial
        primary key,
    name  text not null,
    banknr text not null
        unique
);

create table customers
(
    id    serial
        primary key,
    name  text not null,
    ssn  text not null
        unique,
    approved boolean not null default false
);

create table accounts
(
    id    serial
        primary key,
    customer int not null,
    bank int not null,
    type text not null,
    nr text not null
        unique,
    credit int not null default 0
);

create table transactions
(
    id    serial
        primary key,
    amount  int not null default 0,
    account_nr text not null,
    time TIMESTAMP DEFAULT now(),
    check ( time >= now() )
);

CREATE OR REPLACE FUNCTION check_customer_approved()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM users WHERE id = NEW.id AND is_validated = TRUE
    ) THEN
        RAISE EXCEPTION 'User % is not validated', NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_customer_before_transaction
BEFORE INSERT ON transactions
FOR EACH ROW
EXECUTE FUNCTION check_customer_approved();
