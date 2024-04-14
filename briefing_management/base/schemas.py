from drf_spectacular.openapi import AutoSchema


class AutoSchemaAux:

    def __init__(self, view):
        self.view = view
        self.model = self.get_model()
        self.action = getattr(
            view, "action", self.get_action_from_method()
        )  # Some views don't have action attribute

    def get_action_from_method(self) -> str:
        """
        Returns the action method based on the request method.
        """
        if self.view.request.method == "GET":
            if self._is_retrieve():
                return "retrieve"
            else:
                return "list"
        method_to_action = {
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "destroy",
        }
        return method_to_action.get(self.view.request.method, "")

    def _is_retrieve(self) -> bool:
        return hasattr(self.view, "lookup_field") and self.view.lookup_field == "id"

    def _is_plural(self) -> bool:
        """
        Returns True if the model name is plural.
        """
        return self.action == "list"

    def _get_model_name(self) -> str:
        """
        Returns the model name in title case.
        """
        return self.model._meta.verbose_name

    def _get_model_name_plural(self) -> str:
        """
        Returns the model name in plural.
        """
        return self.model._meta.verbose_name_plural

    def get_model(self):
        """
        Returns the model class of the serializer.
        """
        if hasattr(self.view, "get_serializer_class"):
            return self.view.get_serializer_class().Meta.model
        return None

    def get_response_description_by_status_code(self) -> dict:
        """
        Generates a dictionary of response codes and messages based on the action method and model info.
        """
        if not self.model:
            return {}

        model_name = self._get_model_name().title()
        model_name_plural = self._get_model_name_plural().title()
        error_message = "Erro inesperado"
        responses = {
            "list": {
                "200": f"{model_name_plural} disponíveis",
                "404": f"Não há {model_name.lower()} disponível",
                "400": "Requisição inválida",
                "500": error_message,
            },
            "create": {
                "201": "Criado com sucesso. Id: {id}",
                "400": f"Objeto {model_name} inválido",
                "404": "Caminho inexistente.",
                "500": error_message,
            },
            "update": {
                "200": "Atualizado com sucesso. Id: {id}",
                "400": f"Objeto {model_name} inválido",
                "404": f"{model_name} inexistente.",
                "500": error_message,
            },
            "retrieve": {
                "200": f"{model_name} existe",
                "400": "Requisição inválida",
                "404": f"{model_name} não existe",
                "500": error_message,
            },
        }
        return responses.get(self.action, {})

    def get_summary_action(self) -> str | None:
        """
        Provides a summary description based on the action method type.
        """
        if not self.model:
            return None

        model_name = self._get_model_name().lower()
        model_name_plural = self._get_model_name_plural().lower()
        summaries = {
            "list": f"Busca todos os {model_name_plural}",
            "create": f"Cria um novo {model_name}",
            "update": f"Atualiza um {model_name}",
            "retrieve": f"Busca um {model_name}",
        }
        return summaries.get(self.action)

    def get_operation_id(self) -> str | None:
        """
        Generates a unique operation ID based on the model name and method.
        """
        if not self.model:
            return None

        model_name = (
            self._get_model_name_plural().title()
            if self._is_plural()
            else self._get_model_name().title()
        )
        operation_ids = {
            "list": f"get{model_name.replace(' ', '')}",
            "create": f"post{model_name.replace(' ', '')}",
            "update": f"put{model_name.replace(' ', '')}",
            "retrieve": f"get{model_name.replace(' ', '')}",
        }
        return operation_ids.get(self.action)


class BaseAutoSchema(AutoSchema):

    def get_aux_auth_schema(self) -> AutoSchemaAux:
        if not hasattr(self, "_get_aux_auth_schema"):
            # In the init, the view is not yet set
            self._get_aux_auth_schema = AutoSchemaAux(self.view)
        return self._get_aux_auth_schema

    def get_summary(self) -> str | None:
        return self.get_aux_auth_schema().get_summary_action()

    def get_operation_id(self) -> str:
        operation_id = self.get_aux_auth_schema().get_operation_id()
        return operation_id if operation_id else super().get_operation_id()

    def _get_response_bodies(self):
        """Override description of response bodies and adding those that don't come by default"""
        response_bodies = super()._get_response_bodies()
        descriptions_by_status = (
            self.get_aux_auth_schema().get_response_description_by_status_code()
        )
        for status_code, description in descriptions_by_status.items():
            if status_code in response_bodies:
                response_bodies[status_code]["description"] = description
            else:
                response_bodies[status_code] = {"description": description}

        return response_bodies

    # TODO: Implement tag override method
    # TODO: Implement requestBody override for POST and PUT methods
