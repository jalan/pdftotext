#include <Python.h>
#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-global.h>
#include <poppler/cpp/poppler-page.h>

static PyObject* PdftotextError;

static PyObject*
extract(PyObject* const self, PyObject* const args)
{
    const char* filename;
    const poppler::document* doc;
    const poppler::page* page;
    std::vector<char> doc_utf8;
    std::vector<char> page_utf8;

    // TODO: accept a file-like object instead of a filename

    if (!PyArg_ParseTuple(args, "s", &filename)) {
        return NULL;
    }

    doc = poppler::document::load_from_file(std::string(filename));
    if (doc == NULL) {
        return NULL; // PyErr_SetString already called in callback
    }

    const int page_count = doc->pages();
    for (int i = 0; i < page_count; i++) {
        page = doc->create_page(i);
        if (page == NULL) {
            return NULL; // PyErr_SetString already called in callback
        }
        page_utf8 = page->text().to_utf8();
        doc_utf8.insert(doc_utf8.end(), page_utf8.begin(), page_utf8.end());
    }

    return PyUnicode_DecodeUTF8(doc_utf8.data(), doc_utf8.size(), NULL);
}

static PyMethodDef PdftotextFunctions[] =
{
    {"extract", extract, METH_VARARGS, "Extract text from a PDF."},
    {NULL, NULL, 0, NULL}, // sentinel
};

static struct PyModuleDef pdftotextmodule = {
    PyModuleDef_HEAD_INIT,
    "pdftotext",
    "Simple PDF text extraction.",
    0,
    PdftotextFunctions,
};

static void
error_to_exception(const std::string &message, void*) {
    printf(message.c_str());
    PyErr_SetString(PdftotextError, message.c_str());
}

PyMODINIT_FUNC
PyInit_pdftotext()
{
    PyObject* module;

    module = PyModule_Create(&pdftotextmodule);
    if (module == NULL) {
        return NULL;
    }

    // TODO: Turn poppler's error message into a Python exception?
    //       Or disable those and make our own exceptions?
    poppler::set_debug_error_function(error_to_exception, NULL);

    PdftotextError = PyErr_NewExceptionWithDoc(
        "pdftotext.Error", "Raised when text extraction fails.", NULL, NULL);
    Py_INCREF(PdftotextError);
    PyModule_AddObject(module, "Error", PdftotextError);
    return module;
}
