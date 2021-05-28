CREATE TABLE  IF NOT EXISTS  users (
    id     integer  PRIMARY KEY
                   UNIQUE
                   NOT NULL,
    name   TEXT    NOT NULL,
    worker BOOLEAN NOT NULL,
    staff   BOOLEAN NOT NULL,
    admin  BOOLEAN NOT NULL,
    creator BOOLEAN NOT NULL
);

CREATE TABLE  IF NOT EXISTS  locations (
    id   serial PRIMARY KEY
                 UNIQUE
                 NOT NULL,
    name text    NOT NULL
);


CREATE TABLE IF NOT EXISTS  tools (
    id          serial PRIMARY KEY
                        UNIQUE
                        NOT NULL,
    id_location integer        references locations (id) ON DELETE CASCADE
                        NOT NULL,
    name        text   NOT NULL,
    number      INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS transfers (
    id               serial PRIMARY KEY
                             UNIQUE
                             NOT NULL,
    id_user          INTEGER references users (id) ON DELETE CASCADE
                             NOT NULL,
    id_last_location INTEGER references locations (id) ON DELETE CASCADE
                             NOT NULL,
    id_new_location  INTEGER references locations (id) ON DELETE CASCADE
                             NOT NULL,
    id_tool          INTEGER references tools (id) ON DELETE CASCADE
                             NOT NULL,
    number           INTEGER NOT NULL
);


