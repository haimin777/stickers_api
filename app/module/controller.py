from flask import request, jsonify
from app import app
from .models import *
from .const import HttpStatus

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("<Request: {}>".format(request.json))
    return "<h1>Welcome to Flask Restful API</h1>"




@app.route('/api/v1/codes', methods=['GET', 'POST'])
def promoCodes():
    if request.method == 'GET':
        res = []
        existing_stickers_ids = [item.id for item in Sticker.query.all()]
        print(existing_stickers_ids, '\n'*2)
        for i in existing_stickers_ids:
            pc1 = PromoCode.query.filter_by(sticker_id=i).first()
            if pc1:
                res.append(pc1.value)
        construct = {
            'error': [],
            'success': True,
            'promoCodes': res
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK

    elif request.method == 'POST':
        value = None if request.json['body']['value'] is "" else request.json['body']['value']
        sticker_id = None if request.json['body']['sticker_id'] is "" else request.json['body']['sticker_id']
        construct = {}
        try:
            mhs = PromoCode(value=value, sticker_id=sticker_id)
            mhs.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
            print("<sticker_id: {}, value: {}>".format(sticker_id, value))
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST


    return response


@app.route('/api/v1/stickers', methods=['GET', 'POST'])
def stickers_main():
    if request.method == 'GET':
        res = []
        for sticker in Sticker.query.all():

            res.append(
                        {'Sticker':{'id': sticker.id,
                        'path': sticker.path,
                         'link': sticker.link}
                        }
                        )
        construct = {
            'error': [],
            'success': True,
            'promoCodes': res
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK

    elif request.method == 'POST':
        path = None if request.json['body']['path'] is "" else request.json['body']['path']
        link = None if request.json['body']['link'] is "" else request.json['body']['link']
        construct = {}
        try:
            mhs = Sticker(path=path, link=link)
            mhs.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
            print("<path: {}, link: {}>".format(path, link))
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST


    return response


@app.route('/api/v1/sticker/<string:code>', methods=['GET', 'POST'])
def stickers(code):
    '''
    stickers = Sticker.query.all()
    if request.method == 'GET':
        res = []
        for sticker in stickers:
            construct = {
                'error': [],
                'success': True,
                'Stickers': {
                    'id': sticker.id,
                    'path': sticker.path,
                    'link': sticker.link
                            }
                        }

            res.append(construct)
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
        '''

    if request.method == 'POST':
        code_for_sticker = PromoCode.query.filter_by(value=code).first()

        #find sticker that asociate with this promocode

        sticker = Sticker.query.filter_by(id=code_for_sticker.sticker_id).first()

        construct = {
            'error': [],
            'success': True,
            'Stickers': {
                'id': sticker.id,
                'path': sticker.path,
                'link': sticker.link
                        }
                    }

        response = jsonify(construct)
        response.status_code = HttpStatus.OK

        return response

