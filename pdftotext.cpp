#include <Python.h>

#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-global.h>
#include <poppler/cpp/poppler-page.h>

#include <algorithm>
#include <climits>
#include <string>
#include <vector>


static PyObject* PdftotextError;

typedef struct {
    PyObject_HEAD
    int page_count;
    bool raw;
    PyObject* data;
    poppler::document* doc;
} PDF;

static void PDF_clear(PDF* self) {
    self->page_count = 0;
    self->raw = false;
    delete self->doc;
    self->doc = NULL;
    Py_CLEAR(self->data);
}

static int PDF_set_raw(PDF* self, int raw) {
    if (raw == 0) {
        self->raw = false;
    } else if (raw == 1) {
        self->raw = true;
    } else {
        PyErr_Format(PyExc_ValueError, "a boolean is required");
        return -1;
    }
    return 0;
}

static int PDF_load_data(PDF* self, PyObject* file) {
    #if PY_MAJOR_VERSION >= 3
    self->data = PyObject_CallMethod(file, "read", NULL);
    #else
    self->data = PyObject_CallMethod(file, (char*)"read", NULL);
    #endif
    if (self->data == NULL) {
        return -1;
    }
    return 0;
}

static int PDF_create_doc(PDF* self) {
    Py_ssize_t len;
    char* buf;

    if (PyBytes_AsStringAndSize(self->data, &buf, &len) < 0) {
        return -1;
    }
    if (len > INT_MAX) {
        PyErr_Format(PdftotextError, "invalid buffer length %zd", len);
        return -1;
    }
    self->doc = poppler::document::load_from_raw_data(buf, (int)len);
    if (self->doc == NULL) {
        PyErr_Format(PdftotextError, "poppler error creating document");
        return -1;
    }
    return 0;
}

static int PDF_unlock(PDF* self, char* password) {
    if (self->doc->unlock(std::string(password), std::string(password))) {
        PyErr_Format(PdftotextError, "failed to unlock document");
        return -1;
    }
    return 0;
}

static int PDF_init(PDF* self, PyObject* args, PyObject* kwds) {
    PyObject* pdf_file;
    char* password = (char*)"";
    int raw = 0;
    static char* kwlist[] = {(char*)"pdf_file", (char*)"password", (char*)"raw", NULL};

    PDF_clear(self);
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|si", kwlist, &pdf_file, &password, &raw)) {
        goto error;
    }
    if (PDF_set_raw(self, raw) < 0) {
        goto error;
    }
    if (PDF_load_data(self, pdf_file) < 0) {
        goto error;
    }
    if (PDF_create_doc(self) < 0) {
        goto error;
    }
    if (PDF_unlock(self, password) < 0) {
        goto error;
    }

    self->page_count = self->doc->pages();
    return 0;

error:
    PDF_clear(self);
    return -1;
}

static void PDF_dealloc(PDF* self) {
    PDF_clear(self);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* PDF_read_page(PDF* self, int page_number) {
    const poppler::page* page;
    poppler::page::text_layout_enum layout_mode;
    std::vector<char> page_utf8;

    page = self->doc->create_page(page_number);
    if (page == NULL) {
        return PyErr_Format(PdftotextError, "poppler error creating page");
    }

    // Workaround for poppler bug #94517, fixed in poppler 0.58.0, released 2017-09-01
    const poppler::rectf rect = page->page_rect();
    const int min = std::min(rect.left(), rect.top());
    const int max = std::max(rect.right(), rect.bottom());

    layout_mode = poppler::page::physical_layout;
    if (self->raw) {
        layout_mode = poppler::page::raw_order_layout;
    }
    page_utf8 = page->text(poppler::rectf(min, min, max, max), layout_mode).to_utf8();
    delete page;
    return PyUnicode_DecodeUTF8(page_utf8.data(), page_utf8.size(), NULL);
}

static Py_ssize_t PDF_len(PyObject* obj) {
    PDF* self = (PDF*)obj;
    return self->page_count;
}

static PyObject* PDF_getitem(PyObject* obj, Py_ssize_t i) {
    PDF* self = (PDF*)obj;

    if (i < 0 || i >= self->page_count) {
        return PyErr_Format(PyExc_IndexError, "index out of range");
    }
    return PDF_read_page(self, (int)i);
}

static PySequenceMethods PDF_sequence_methods = {
    PDF_len,      // sq_length (__len__)
    0,            // sq_concat
    0,            // sq_repeat
    PDF_getitem,  // sq_item (__getitem__)
};

static PyTypeObject PDFType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pdftotext.PDF",                                                // tp_name
    sizeof(PDF),                                                    // tp_basicsize
    0,                                                              // tp_itemsize
    (destructor)PDF_dealloc,                                        // tp_dealloc
    0,                                                              // tp_print
    0,                                                              // tp_getattr
    0,                                                              // tp_setattr
    0,                                                              // tp_reserved
    0,                                                              // tp_repr
    0,                                                              // tp_as_number
    &PDF_sequence_methods,                                          // tp_as_sequence
    0,                                                              // tp_as_mapping
    0,                                                              // tp_hash
    0,                                                              // tp_call
    0,                                                              // tp_str
    0,                                                              // tp_getattro
    0,                                                              // tp_setattro
    0,                                                              // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                       // tp_flags
    "PDF(pdf_file, password=\"\", raw=False)\n"
    "\n"
    "Args:\n"
    "    pdf_file: A file opened for reading in binary mode.\n"
    "    password: Unlocks the document, if required. Either the owner\n"
    "        password or the user password works.\n"
    "    raw: If True, page text is output in the order it appears in the\n"
    "        content stream, rather than in the order it appears on the\n"
    "        page.\n"
    "\n"
    "Example:\n"
    "    with open(\"doc.pdf\", \"rb\") as f:\n"
    "        pdf = PDF(f)\n"
    "    for page in pdf:\n"
    "        print(page)",                                          // tp_doc
    0,                                                              // tp_traverse
    0,                                                              // tp_clear
    0,                                                              // tp_richcompare
    0,                                                              // tp_weaklistoffset
    0,                                                              // tp_iter
    0,                                                              // tp_iternext
    0,                                                              // tp_methods
    0,                                                              // tp_members
    0,                                                              // tp_getset
    0,                                                              // tp_base
    0,                                                              // tp_dict
    0,                                                              // tp_descr_get
    0,                                                              // tp_descr_set
    0,                                                              // tp_dictoffset
    (initproc)PDF_init,                                             // tp_init
};

#if POPPLER_CPP_AT_LEAST_0_30_0
static void do_nothing(const std::string&, void*) {}
#endif

#if PY_MAJOR_VERSION >= 3
static PyModuleDef pdftotextmodule = {
    PyModuleDef_HEAD_INIT,
    "pdftotext",
    "Simple PDF text extraction.",
};

PyMODINIT_FUNC PyInit_pdftotext() {
    PyObject* module;

    PDFType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&PDFType) < 0) {
        return NULL;
    }

    module = PyModule_Create(&pdftotextmodule);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&PDFType);
    PyModule_AddObject(module, "PDF", (PyObject*)&PDFType);

    PdftotextError = PyErr_NewExceptionWithDoc(
        "pdftotext.Error", "PDF error.", NULL, NULL);
    Py_INCREF(PdftotextError);
    PyModule_AddObject(module, "Error", PdftotextError);

    #if POPPLER_CPP_AT_LEAST_0_30_0
    poppler::set_debug_error_function(do_nothing, NULL);
    #endif

    return module;
}
#else
PyMODINIT_FUNC initpdftotext() {
    PyObject* module;

    PDFType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&PDFType) < 0) {
        return;
    }

    module = Py_InitModule3("pdftotext", NULL, "Simple PDF text extraction.");
    if (module == NULL) {
        return;
    }

    Py_INCREF(&PDFType);
    PyModule_AddObject(module, "PDF", (PyObject*)&PDFType);

    PdftotextError = PyErr_NewExceptionWithDoc(
        (char*)"pdftotext.Error", (char*)"PDF error.", NULL, NULL);
    Py_INCREF(PdftotextError);
    PyModule_AddObject(module, "Error", PdftotextError);

    #if POPPLER_CPP_AT_LEAST_0_30_0
    poppler::set_debug_error_function(do_nothing, NULL);
    #endif
}
#endif
