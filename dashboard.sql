CREATE TABLE events (
	id SERIAL PRIMARY KEY,
	node_vk VARCHAR(255) NOT NULL,
	event VARCHAR(255) NOT NULL,
	event_info VARCHAR(255),
	timestamp timestamp NOT NULL DEFAULT NOW()

);