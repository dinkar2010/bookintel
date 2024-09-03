create table books(
    id BIGSERIAL PRIMARY KEY UNIQUE NOT NULL,
    title text UNIQUE NOT NULL,
    genre text,
    year_published DATE NOT NULL,
    summary text
);

create table reviews(
    id BIGSERIAL PRIMARY KEY UNIQUE NOT NULL,
    book_id BIGSERIAL REFERENCES books(id) ON DELETE CASCADE,
    reviewer varchar(32) NOT NULL,
    content text,
    rating DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 5)
);