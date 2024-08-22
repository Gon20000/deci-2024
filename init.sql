CREATE TABLE IF NOT EXISTS coaches (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TINYTEXT NOT NULL,
  age INTEGER NOT NULL,
  gender TINYTEXT CHECK (gender in ("Male", "Female")),
  price INTEGER NOT NULL,
  experience INTEGER NOT NULL,
  rating DECIMAL(3, 1) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS athletes (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TINYTEXT NOT NULL,
  age INTEGER NOT NULL,
  gender TINYTEXT CHECK (gender in ("Male", "Female")),
  club TINYTEXT NOT NULL,
  sport TINYTEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS availability (
  id INTEGER PRIMARY KEY,
  coachID INTEGER NOT NULL,
  available_date DATE NOT NULL,

  FOREIGN KEY(coachID) REFERENCES coaches(id)
  UNIQUE (coachID, available_date)
);


CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY,
  availabilityID INTEGER NOT NULL,
  athleteID INTEGER NOT NULL,

  FOREIGN KEY(availabilityID) REFERENCES availability(id),
  FOREIGN KEY(athleteID) REFERENCES athletes(id),
  UNIQUE (availabilityID, athleteID)
);
