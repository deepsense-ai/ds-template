import {{ cookiecutter.__package_name }}.hello


def test_basic_test() -> None:
    {{ cookiecutter.__package_name }}.hello.hello_world()
    assert True
