import pytest
from numpy.testing import assert_allclose
import chainladder as cl


@pytest.fixture
def atol():
    return 1e-5


data = ['RAA', 'ABC', 'GenIns', 'MW2008', 'MW2014']


@pytest.mark.parametrize('data', data)
def test_benktander_to_chainladder(data, atol):
    tri = cl.load_dataset(data)
    a = cl.Chainladder().fit(tri).ibnr_
    b = cl.Benktander(apriori=.8, n_iters=255).fit(tri, sample_weight=a).ibnr_
    assert_allclose(a.triangle, b.triangle, atol=atol)


def test_bf_eq_cl_when_using_cl_apriori():
    cl_ult = cl.Chainladder().fit(cl.load_dataset('quarterly')).ultimate_
    cl_ult.rename('development', ['apriori'])
    bf_ult = cl.BornhuetterFerguson().fit(cl.load_dataset('quarterly'),
                                          sample_weight=cl_ult).ultimate_
    assert_allclose(cl_ult.triangle, bf_ult.triangle, atol=1e-5)
