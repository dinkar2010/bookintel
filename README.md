# Book Intelligence System

## Overview
The Book Intelligence System is a platform designed to analyze and extract meaningful insights from large collections of books. This system can generate summaries, identify key themes. It provide interface to add reiviews for the book.

## Features
* Listing Book: Add/Create New book
* Reviews: Add review for books
* Summary: Generate summary based on the content

### Required Parameter for the book and review POST request:
* books(title, genre, year_published,summary text)
* reviews(reviewer, content, rating(in range of 0-5 inclusive)

## Installation
  ### Prerequisites
    Python 3.10+
    pip3

  ### Installation of python packages:
    pip3 install -r requirements.txt

## API
* GET /books               :List the saved books
* POST /books              :Add new book
* GET /books/<id>          :Fetch the book details by id)
* PUT /books/<id>          :Update the book attributes)
* GET /book/<id>/reviews   :Fetch all the reviews of a book
* POST /book/<id>/reviews  :Add new review of book by id
* GET /books/<id>/summary  :Get Summary of a book
* POST /generate-summary     :Generate Summary based on content
