#-*- coding: utf-8 -*-
import unittest, io, sys


# To hell with the module system. I know what I'm doing (probably).
if sys.version_info[0] == 2:
    import imp
    py = imp.load_source('py', 'bin/py')
else:
    from importlib.machinery import SourceFileLoader
    py = SourceFileLoader("py", "bin/py").load_module()


class DetectModeInMinimalExpr(unittest.TestCase):
    def runTest(self):
        self.assertEqual(py.detect_mode(''), py.ExecMode.ONCE)
        self.assertEqual(py.detect_mode('input'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('binput'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('lines'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('blines'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('line'), py.ExecMode.EACH_LINE)
        self.assertEqual(py.detect_mode('bline'), py.ExecMode.EACH_LINE)

class DetectModeInSimpleExpr(unittest.TestCase):
    def runTest(self):
        self.assertEqual(py.detect_mode('10 ** 4 + 3'), py.ExecMode.ONCE)
        self.assertEqual(py.detect_mode('input.method(a, b)'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('binput.method(a, b)'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('lines.method(a, b)'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('blines.method(a, b)'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('line.method(a, b)'), py.ExecMode.EACH_LINE)
        self.assertEqual(py.detect_mode('bline.method(a, b)'), py.ExecMode.EACH_LINE)

class DetectModeInComplexExpr(unittest.TestCase):
    def runTest(self):
        self.assertEqual(py.detect_mode('map(x, lambda x: f(y).m() + x)'), py.ExecMode.ONCE)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(input).m() + x)'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(binput).m() + x)'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(lines).m() + x)'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(blines).m() + x)'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(line).m() + x)'), py.ExecMode.EACH_LINE)
        self.assertEqual(py.detect_mode('map(x, lambda x: f(bline).m() + x)'), py.ExecMode.EACH_LINE)

class DetectModeInMultiVarExpr(unittest.TestCase):
    def runTest(self):
        self.assertEqual(py.detect_mode('input and binput'), py.ExecMode.ONCE_INPUT)
        self.assertEqual(py.detect_mode('lines and blines'), py.ExecMode.ONCE_LINES)
        self.assertEqual(py.detect_mode('line and bline'), py.ExecMode.EACH_LINE)

class DetectModeFailWithIncompatibleMultiVarExpr(unittest.TestCase):
    def runTest(self):
        with self.assertRaises(py.AbortException):
            py.detect_mode('input and line')

class ExecuteReturnsCorrectType(unittest.TestCase):
    def runTest(self):
        results = execute('binput', stream_bytes("🫢"))
        self.assertEqual(results, [b'\xf0\x9f\xab\xa2'])

        results = execute('input', stream_text("🫢"))
        self.assertEqual(results, [py.to_text("🫢", 'utf-8')])

class ExecuteRemovesNewlines(unittest.TestCase):
    def runTest(self):
        results = execute('line', stream_text("Yep\nNope\nHa"))
        self.assertEqual(results, ["Yep", "Nope", "Ha"])

class ExecuteDoesTheThing(unittest.TestCase):
    def runTest(self):
        # I don't really know what's the best thing to do here. Well, honestly, I'm OK with just
        # covering some ground. This isn't a military-grade tool.

        expr = '"yes" if binput == b"\x41" else "no"'
        self.assertEqual(execute(expr, stream_bytes("A")), ["yes"])
        self.assertEqual(execute(expr, stream_bytes("x")), ["no"])

        expr = '"\\n".join("foo" + l for l in lines)'
        in_lines = ["This", "has", "four", "lines"]
        out_lines = [ "\n".join([ "foo" + line for line in in_lines ]) ]
        self.assertEqual(execute(expr, stream_text("\n".join(in_lines))), out_lines)

        expr = '"foo " + line'
        in_lines = ["This", "has", "four", "lines"]
        out_lines = [ "foo " + line for line in in_lines ]
        self.assertEqual(execute(expr, stream_text("\n".join(in_lines))), out_lines)
        

def execute(expr, stream):
    return list(py.execute(expr, py.detect_mode(expr), stream, 'utf-8'))

def stream_bytes(text):
    return io.BytesIO(py.to_binary(text, 'utf-8'))

def stream_text(text):
    return io.StringIO(py.to_text(text, 'utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)