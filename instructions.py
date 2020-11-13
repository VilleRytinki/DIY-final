from flask_restful import Resource
from http import HTTPStatus
from flask import request

from instruction import Instruction

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional


class InstructionListRecourse(Resource):
    def get(self):
        instructions = Instruction.get_all_published()

        data = []
        for instruction in instructions:
            data.append(instruction.data())
        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()

        instruction = Instruction(json_data['name'], json_data['description'], json_data['steps'], json_data['tools'],
                                  json_data['cost'],
                                  json_data['duration'])

        instruction.save()

        return instruction.data, HTTPStatus.CREATED


class InstructionResource(Resource):
    def get(self, instruction_id):

        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if instruction.is_publish == False and instruction.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return instruction.data(), HTTPStatus.OK

    @jwt_required
    def put(self, instruction_id):
        json_data = request.get_json()

        instruction = Instruction(json_data['name'], json_data['description'], json_data['steps'], json_data['tools'],
                                  json_data['cost'],
                                  json_data['duration'])

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.name = json_data['name']
        instruction.description = json_data['description']
        instruction.steps = json_data['steps']
        instruction.tools = json_data['tools']
        instruction.cost = json_data['cost']
        instruction.duration = json_data['duration']

        instruction.save()

        return instruction.data, HTTPStatus.OK

    @jwt_required
    def delete(self, instruction_id):
        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if instruction.is_publish == False and instruction.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.delete()

        return {}, HTTPStatus.NO_CONTENT


class InstructionPublic(Resource):
    def put(self, instruction_id):
        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = True

        return {}, HTTPStatus.NO_CONTENT


    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instructions_list if instruction.id ==
                            instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
