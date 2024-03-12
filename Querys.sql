
-- Crear tabla Chains
CREATE TABLE Chains (
    chid SERIAL PRIMARY KEY,
    cname VARCHAR NOT NULL,
    springmkup FLOAT NOT NULL,
    summermkup FLOAT NOT NULL,
    fallmkup FLOAT NOT NULL,
    wintermkup FLOAT NOT NULL
);

-- Crear tabla Hotel, incluyendo la clave foránea para Chains
CREATE TABLE Hotel (
    hid SERIAL PRIMARY KEY,
    chid INTEGER,
    hname VARCHAR NOT NULL,
    hcity VARCHAR NOT NULL,
    CONSTRAINT fk_hotel_chains FOREIGN KEY (chid) REFERENCES Chains(chid)
);

-- Crear tabla Employee, incluyendo la clave foránea para Hotel
CREATE TABLE Employee (
    eid SERIAL PRIMARY KEY,
    hid INTEGER,
    fname VARCHAR NOT NULL,
    lname VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    salary FLOAT NOT NULL,
    position VARCHAR NOT NULL,
    CONSTRAINT fk_employee_hotel FOREIGN KEY (hid) REFERENCES Hotel(hid)
);

-- Crear tabla RoomDescription
CREATE TABLE RoomDescription (
    rdid SERIAL PRIMARY KEY,
    rname VARCHAR NOT NULL,
    rtype VARCHAR NOT NULL,
    capacity INTEGER NOT NULL,
    ishandicap BOOLEAN NOT NULL
);

-- Crear tabla Room, incluyendo las claves foráneas para Hotel y RoomDescription
CREATE TABLE Room (
    rid SERIAL PRIMARY KEY,
    hid INTEGER,
    rdid INTEGER,
    rprice FLOAT NOT NULL,
    CONSTRAINT fk_room_hotel FOREIGN KEY (hid) REFERENCES Hotel(hid),
    CONSTRAINT fk_room_roomdescription FOREIGN KEY (rdid) REFERENCES RoomDescription(rdid)
);

-- Crear tabla RoomUnavailable, incluyendo la clave foránea para Room
CREATE TABLE RoomUnavailable (
    ruid SERIAL PRIMARY KEY,
    rid INTEGER,
    startdate DATE NOT NULL,
    enddate DATE NOT NULL,
    CONSTRAINT fk_roomunavailable_room FOREIGN KEY (rid) REFERENCES Room(rid)
);

-- Crear tabla Client
CREATE TABLE Client (
    clid SERIAL PRIMARY KEY,
    fname VARCHAR NOT NULL,
    lname VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    memberyear INTEGER NOT NULL
);

-- Crear tabla Reserve, incluyendo las claves foráneas para RoomUnavailable y Client
CREATE TABLE Reserve (
    reid SERIAL PRIMARY KEY,
    ruid INTEGER,
    clid INTEGER,
    total_cost FLOAT NOT NULL,
    payment VARCHAR NOT NULL,
    guests INTEGER NOT NULL,
    CONSTRAINT fk_reserve_roomunavailable FOREIGN KEY (ruid) REFERENCES RoomUnavailable(ruid),
    CONSTRAINT fk_reserve_client FOREIGN KEY (clid) REFERENCES Client(clid)
);

-- Crear tabla Login, incluyendo la clave foránea para Employee
CREATE TABLE Login (
    lid SERIAL PRIMARY KEY,
    eid INTEGER UNIQUE NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    CONSTRAINT fk_login_employee FOREIGN KEY (eid) REFERENCES Employee(eid)
);
