from flask import request, jsonify
from flasgger import swag_from
from http import HTTPStatus
from ..app import app
from marshmallow.exceptions import ValidationError
from ..schemas.schmas import CommentSchema
from ..models import Comment


# {
#     "id": 1,
#     'post_id': 2,
#     'content': 'sandkf',
#     'comments': [{
#         'content': 'sdkfd',
#
#     },
#     {
#         'content': 'sdkfd',
#     },
#     {
#         'content': 'sdkfd',
#     },
#     {
#         'content': 'sdkfd',
#     }
#     ]
# }

@app.route('/api/posts/<int:id>/comments/', methods=['GET', 'POST'])
def comments(id):
    if request.method == 'POST':
        try:
            data = request.json or request.form
            serializer = CommentSchema()
            user_id = 1
            comment_data = serializer.load(data)
            content = comment_data['content']
            parent_comment_id = comment_data.get('parent_comment')
            comment_obj = Comment(user_id=user_id, post_id=id, content=content)
            comment_obj.save()
            if parent_comment_id:
                parent_comment = Comment.objects.get_or_404(id=parent_comment_id)
                comment_dict = CommentSchema().dump(comment_obj)
                # comment_dict.update({'_id': str(comment_obj.id)})
                parent_comment.comments.append(comment_dict)
                parent_comment.save()
            return CommentSchema().jsonify(comment_obj), HTTPStatus.CREATED
        except ValidationError as err:
            return jsonify({ 'message': err }), 400
    else:
        comments = Comment.objects.filter(post_id=id)
        return CommentSchema(many=True).jsonify(comments), HTTPStatus.OK
