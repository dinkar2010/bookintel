from sqlalchemy import func
from app.intel.models import engine, BOOKS, REVIEWS
import traceback
from sqlalchemy.orm import scoped_session, sessionmaker
from .content_utils import get_content_summary

def error_msg_respoonse(status_code, msg):
    return {'status_code': status_code, 'details': msg}

def add_new_book(data):
    status_code = 201
    details = 'New book added'
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        session.query(BOOKS).filter(title=data['title']).one()
        status_code = 409
        details =  "Book with the title already exist"
    except:
        try:
            book = BOOKS(
                title=data['title'],
                genre=data['genre'],
                year_published=data['year_published'],
                summary=data['summary']
            )
            session.add(book)
            session.commit()
        except:
            status_code = 201
            details = 'Error in adding new entry'
    session.close()

    return status_code, {'details': details}

def process_book_query_obj(qObj):
    return {
        'id': qObj[0], 'title': qObj[1], 'genre': qObj[2],'year_published': qObj[3],
        'summary': qObj[4]
    }

def process_reviewer_query_obj(rObj):
    return {'id': rObj[0], 'reviewer': rObj[1],'content': rObj[2], 'rating': rObj[3]}

def get_books():
    status_code = 500
    details =  'Internal Server Error'
    try:
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        bookObjs = session.query(BOOKS.id, BOOKS.title, BOOKS.genre, BOOKS.year_published,
                             BOOKS.summary).all()
        session.close()
        data = []
        for d in bookObjs:
            jd = process_book_query_obj(d)
            data.append(jd)
        return 200, {'data': data}
    except:
        traceback.print_exc()
    return status_code, {'details': details}

def get_book_by_id(book_id):
    try:
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        qObj = session.query(BOOKS.id, BOOKS.title, BOOKS.genre, BOOKS.year_published,
                             BOOKS.summary).filter(BOOKS.id==book_id).one()
        session.close()
        return 200, {'data': process_book_query_obj(qObj)}
    except:
        details = 'No row was found when one was required'
    return 500, {'details': details}

def update_book(book_id, data):
    try:
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        bookObj = session.query(BOOKS).filter(BOOKS.id==book_id).one()
        bookObj.title = data.get('title', '') or bookObj.title
        bookObj.genre = data.get('genre', '') or bookObj.genre
        bookObj.year_published = data.get('year_published', '') or bookObj.year_published
        bookObj.summary = data.get('summary', '') or bookObj.summary
        session.commit()
        session.close()
        return 200, {'deatils': 'Details updated successfuly'}
    except:
        pass
    return 404, {'details': 'No row was found when one was required'}

def delete_book_by_id(book_id):
    status_code = 500
    details = 'Internal Server Error'
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        bookObj = session.query(BOOKS).filter(BOOKS.id==book_id).one()
        if not bookObj:
            status_code = 404
            details = 'No such Book!'
        else:
            session.delete(bookObj)
            session.commit()
            status_code = 200
            details= "Book deleted successfully"
    except:
        traceback.print_exc()
        status_code = 400
        details = 'Bad request'
    session.close()
    return status_code, {'details': details}

def get_book_review(book_id):
    status_code = 500
    details = 'Internal Server Error'
    data = []
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        session.query(BOOKS).filter(BOOKS.id==book_id).one()
    except:
        status_code = 404
        details = 'No such Book!'

    try:
        review_list = session.query(REVIEWS.id, REVIEWS.reviewer, REVIEWS.content,
                                    REVIEWS.rating).join(BOOKS).filter(BOOKS.id==book_id).all()

        for d in review_list:
            jd = process_reviewer_query_obj(d)
            data.append(jd)
        status_code = 200
        return status_code, {'data': data}
    except:
        traceback.print_exc()
    session.close()

    if status_code == 200:
        return status_code, {'data': data}

    return status_code, {'details': details}

def add_new_review(book_id, data):
    status_code = 500
    details = 'Internal Server Error'
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        session.query(BOOKS).filter(BOOKS.id==book_id).one()
        try:
            review = REVIEWS(
                book_id=book_id,
                reviewer=data['reviewer'],
                content=data.get('content', ''),
                rating= data.get('rating', 0)
            )
            session.add(review)
            session.commit()
            status_code = 201
            details = 'New review added'
        except Exception as e:
            status_code = 400
            details = "Bad request! rating should be in range of [1, 5]"
    except:
        status_code = 404
        details = 'No such Book!'
    session.close()
    return status_code, {'details': details}

def book_summary(book_id):
    status_code = 200
    details =  'Internal Server Error'
    summary = ""
    avgRating = 0
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        summary = session.query(BOOKS.summary).filter(BOOKS.id==book_id).one()[0]
        avgrating = session.query(func.avg(REVIEWS.rating)).join(BOOKS).filter(BOOKS.id==book_id).scalar() or 0
        avgRating = round(avgrating,1)
    except Exception as e:
        status_code = 404
        details = 'No such Book!'
    session.close()
    if status_code != 200:
        return status_code, {'details': details}
    return status_code, {
        'summary': summary,
        'ratings': avgRating
    }

def generate_summary(content):
    details =  'Internal Server Error'
    if len(content) <= 10:
        return 200, {'summary': content}

    try:
        summary = get_content_summary(content)
        status_code = 200
    except:
        traceback.print_exc()
        status_code = 500

    if status_code != 200:
        return status_code, {
            'details': details
        }
    return status_code, {'summary': summary}