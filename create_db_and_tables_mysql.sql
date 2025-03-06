CREATE TABLE IF NOT EXISTS recipe(
	id INT NOT NULL,
	name VARCHAR(100) NOT NULL,
	nb_person INT,
	sweet_salt VARCHAR(5) DEFAULT NULL,
	time_preparation INT DEFAULT NULL,
	time_rest INT DEFAULT NULL,
	time_cooking INT DEFAULT NULL,
	time_total INT DEFAULT NULL,
	difficulty VARCHAR(20) DEFAULT NULL,
	cost VARCHAR(20) DEFAULT NULL,
	image_link TEXT DEFAULT NULL,
	catalog TINYINT(1),
	country VARCHAR(255),
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS ingredient(
	id INT AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	type VARCHAR (50),
	category VARCHAR(50),
	weigh INT,
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS ingredient_recipe(
	id_recipe INT NOT NULL,
	id_ingredient INT NOT NULL,
	quantity FLOAT,
	unit VARCHAR(50),
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	FOREIGN KEY(id_ingredient) REFERENCES ingredient(id),
	PRIMARY KEY(id_recipe, id_ingredient)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS step(
	id INT AUTO_INCREMENT,
	id_recipe INT NOT NULL,
	step_number INT NOT NULL,
	detail TEXT,
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS users(
	id VARCHAR(255) not NULL,
	name VARCHAR(255) NOT NULL,
	nb_person INT,
	week_lunch TINYINT(1),
	week_we TINYINT(1),
	diet VARCHAR(255) DEFAULT NULL,
	aversion VARCHAR(255) DEFAULT NULL,
	intolerance VARCHAR(255),
	picture varchar(255),
	lunch_sizes varchar(15),
	dinner_sizes varchar(15),
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS user_recipe(
	id_user VARCHAR(255) NOT NULL,
	id_recipe INT NOT NULL,
	planner TINYINT(1),
	lunch_size int default 0,
	dinner_size int default 0,
	FOREIGN KEY(id_user) REFERENCES users(id),
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	PRIMARY KEY(id_recipe, id_user)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
