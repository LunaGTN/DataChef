CREATE DATABASE datachef;

USE datachef;

CREATE TABLE recipe(
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
	catalog BOOLEAN,
	PRIMARY KEY(id)
);

CREATE TABLE ingredient(
	id INT NOT NULL,
	name VARCHAR(100) NOT NULL,
	type VARCHAR (50),
	PRIMARY KEY(id)
);


CREATE TABLE ingredient_recipe(
	id_recipe INT NOT NULL,
	id_ingredient INT NOT NULL,
	quantity FLOAT,
	unit VARCHAR(50),
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	FOREIGN KEY(id_ingredient) REFERENCES ingredient(id),
	PRIMARY KEY(id_recipe, id_ingredient)
);


CREATE TABLE step(
	id INT AUTO_INCREMENT,
	id_recipe INT NOT NULL,
	step_number INT NOT NULL,
	detail TEXT,
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	PRIMARY KEY(id)
);


CREATE TABLE user(
	id VARCHAR(36) DEFAULT (UUID()),
	pseudo VARCHAR(255) NOT NULL,
	nb_person INT,
	diet VARCHAR(255) DEFAULT NULL,
	aversion VARCHAR(255) DEFAULT NULL,
	intolerance VARCHAR(255),
	PRIMARY KEY(id)
);


CREATE TABLE user_recipe(
	id_user VARCHAR(36) NOT NULL,
	id_recipe INT NOT NULL,
	FOREIGN KEY(id_user) REFERENCES user(id),
	FOREIGN KEY(id_recipe) REFERENCES recipe(id),
	PRIMARY KEY(id_recipe, id_user)
);


