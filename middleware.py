from flask import jsonify, abort, make_response, request
from data_provider_service import DataProviderService
from utilities import convert_to_title_case

DATA_PROVIDER = DataProviderService()


# get all posts
def read_posts():
    posts = DATA_PROVIDER.get_post_with_author()
    return jsonify({"posts": posts})


# get post by id
def read_post_by_id(post_id):
    current_post = DATA_PROVIDER.get_post_with_author(post_id)
    if current_post:
        return jsonify({"post": current_post})
    else:
        # In case we did not find the post by id
        # we send HTTP 404 - Not Found error to the client
        abort(404)


def create_post():
    userid = 1
    try:
        data = request.get_json(force=True)
        title = data['title']
        content = data['content']
        userid = data['userid']
        if userid is None:
            userid = 1
    except Exception as exc:
        print(exc)

    # uses a utilities class to correctly capitalise the title string
    formatted_title = convert_to_title_case(title)
    formatted_content = (str(content))[:1].upper() + (str(content))[1:]

    new_post_id = DATA_PROVIDER.add_post(title=formatted_title, content=formatted_content, author_id=userid)

    created_post = DATA_PROVIDER.get_post_with_author(new_post_id)
    if created_post:
        return jsonify({"post": created_post})
    else:
        # In case we did not find the post by id
        # we send HTTP 404 - Not Found error to the client
        abort(404)


# update a post
def update_post(post_id):
    try:
        data = request.get_json(force=True)
        print(data)
        title = data['title']
        content = data['content']
    except Exception as exc:
        print(exc)

    formatted_title = convert_to_title_case(title)
    formatted_content = (str(content))[:1].upper() + (str(content))[1:]

    new_post = {
        "title": formatted_title,
        "content": formatted_content
    }
    updated_post = DATA_PROVIDER.update_post(post_id, new_post)
    if not updated_post:
        return make_response('', 404)
    else:
        return jsonify({"post": updated_post})


def register():
    new_user_id = None
    try:
        data = request.get_json(force=True)
        username = data['username']
        password = data['password']
        if username and password:
            new_user_id = DATA_PROVIDER.add_user(username, password)
    except Exception as exc:
        print(exc)
    # if the user is already taken the ID is (0,)
    if new_user_id != (0,):
        return jsonify({"user": new_user_id})
    else:
        abort(404)


def login():
    user = None
    try:
        data = request.get_json(force=True)
        username = data['username']
        password = data['password']
        if username and password:
            user = DATA_PROVIDER.is_user_valid(username, password)
    except Exception as exc:
        print(exc)

    if user is not None:
        resp = make_response(jsonify({'id': user[0],'username': user[1]}), 200)
        return resp
    else:
        abort(404)



# get post by title
def read_post_by_title(title):
    posts = DATA_PROVIDER.get_post_by_title(title)
    if posts:
        return jsonify({"posts": posts})
    else:
        abort(404)