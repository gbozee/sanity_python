import requests


class SanityError(Exception):
    def __init__(self, *args: object) -> None:
        self.error = args[0]
        super().__init__(*args)


class SanityResult:
    def __init__(self, ms=None, query=None, result=None):
        self.ms = ms
        self.query = query
        self.result = result

    def __repr__(self) -> str:
        return "<{}>".format(self.__class__.__name__)


class SanityClient:
    def __init__(
        self,
        project_id: str,
        api_version="v2021-10-21",
        api_key=None,
        dataset="production",
    ) -> None:
        """Initialize the sanity client class

        Args:
            project_id (str): _description_
            api_version (str, optional): _description_. Defaults to "v2021-10-21".
            api_key (_type_, optional): _description_. Defaults to None.
            dataset (str, optional): _description_. Defaults to "production".
        """
        self.dataset = dataset
        self.project_id = project_id
        self.api_version = api_version
        self.api_key = api_key

    def _build_base_url(self, kind):
        return "https://{}.{}.sanity.io/{}/data/query/{}".format(
            self.project_id, kind, self.api_version, self.dataset
        )

    @property
    def base_url(self):
        return self._build_base_url("api")

    @property
    def cdn_base_url(self):
        return self._build_base_url("apicdn")

    def make_query(self, query, params=None):
        """Post query to the cdn version of sanity

        Args:
            query (str): GROQ querysrting
            params (dict, optional): Additional parameters to be sent. Defaults to None.

        Raises:
            SanityError: When request returns status code < 400
            SanityError: When request was successfull but an error key exists in response

        Returns:
            SanityResult
        """
        payload = {"query": query}
        if params and type(params, dict):
            payload["params"] = params
        response = requests.post(self.cdn_base_url, json=payload)
        if response.status_code < 400:
            result = response.json()
            if result.get("error"):
                raise SanityError(result["error"])
            return SanityResult(**result)
        raise SanityError("Error making call")
