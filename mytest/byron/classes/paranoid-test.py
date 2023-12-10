import byron as byron


class MyParanoid(byron.classes.Paranoid):
    pass


class TestParanoid:
    def test_run_paranoia_checks(self):
        paranoid = MyParanoid()
        assert paranoid.run_paranoia_checks() == True
