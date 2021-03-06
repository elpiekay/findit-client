import os
import pytest

from findit_client import FindItClient

TARGET_PATH = r'tests/pics/screen.png'
TEMPLATE_NAME = r'wechat_logo.png'
PORT = 9410

pic_root = os.path.join(os.path.dirname(__file__), 'pics')
cli = None


@pytest.fixture(scope="session", autouse=True)
def run_at_beginning(request):
    global cli
    cli = FindItClient(local_mode=True, pic_root=pic_root, python_path='python')
    yield
    cli.local_server.stop()


def test_heartbeat():
    assert cli.heartbeat()


def test_analyse_with_path():
    result = cli.analyse_with_path(TARGET_PATH, TEMPLATE_NAME)

    arg_list = ['msg', 'status', 'request', 'response', 'data']
    for each in arg_list:
        assert hasattr(result, each)


def test_analyse_with_extras():
    result = cli.analyse_with_path(
        TARGET_PATH, TEMPLATE_NAME,
        a='123', b='456', pro_mode=True, engine_template_scale=(1, 4, 10))

    request_dict = result.request

    assert 'extras' in request_dict
    assert 'a' in request_dict['extras']
    assert 'b' in request_dict['extras']
    assert 'engine_template_scale' in request_dict['extras']

    template_result = result.template_engine
    assert template_result.get_conf(TEMPLATE_NAME)['engine_template_scale'] == [1, 4, 10]


def test_template_engine():
    result = cli.analyse_with_path(TARGET_PATH, TEMPLATE_NAME)
    template_result = result.template_engine

    assert template_result.get_target_sim(TEMPLATE_NAME) > 0.9
    assert template_result.get_target_point(TEMPLATE_NAME)


def test_template_engine_without_target_name():
    result = cli.analyse_with_path(TARGET_PATH, TEMPLATE_NAME)
    template_result = result.template_engine

    assert template_result.get_target_sim() > 0.9
    assert template_result.get_target_point()


def test_feature_engine():
    result = cli.analyse_with_path(TARGET_PATH, TEMPLATE_NAME)
    feature_result = result.feature_engine

    assert feature_result.get_target_point(TEMPLATE_NAME) != [-1, -1]
