#include <Python.h>
#include <structmember.h>

#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-global.h>
#include <poppler/cpp/poppler-page.h>

#include <string>
#include <vector>


static PyObject* PdftotextError;

typedef struct {
    PyObject_HEAD
    int page_count;
    PyObject* data;
    poppler::document* doc;
} PDF;

static PyMemberDef PDF_members[] = {
    {
        (char*)"page_count",
        T_INT,
        offsetof(PDF, page_count),
        READONLY,
        (char*)"Page count.",
    },
    {NULL},  // Sentinel
};

static void PDF_clear(PDF* self) {
    self->page_count = 0;
    delete self->doc;
    self->doc = NULL;
    Py_CLEAR(self->data);
}

static int PDF_load_data(PDF* self, PyObject* args, PyObject* kwds) {
    PyObject* arg;
    static char* kwlist[] = {(char*)"pdf_file", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &arg)) {
        return -1;
    }
    #if PY_MAJOR_VERSION >= 3
    self->data = PyObject_CallMethod(arg, "read", NULL);
    #else
    self->data = PyObject_CallMethod(arg, (char*)"read", NULL);
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
        Py_CLEAR(self->data);
        return -1;
    }
    self->doc = poppler::document::load_from_raw_data(buf, len);
    if (self->doc == NULL) {
        PyErr_Format(PdftotextError, "Poppler error creating document");
        Py_CLEAR(self->data);
        return -1;
    }
    return 0;
}

static int PDF_init(PDF* self, PyObject* args, PyObject* kwds) {
    PDF_clear(self);
    if (PDF_load_data(self, args, kwds) < 0) {
        return -1;
    }
    if (PDF_create_doc(self) < 0) {
        return -1;
    }
    self->page_count = self->doc->pages();
    return 0;
}

static void PDF_dealloc(PDF* self) {
    PDF_clear(self);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* PDF_read_page(PDF* self, int page_number) {
    const poppler::page* page;
    std::vector<char> page_utf8;

    page = self->doc->create_page(page_number - 1);
    if (page == NULL) {
        return PyErr_Format(PdftotextError, "Poppler error creating page");
    }
    page_utf8 = page->text().to_utf8();
    delete page;
    return PyUnicode_DecodeUTF8(page_utf8.data(), page_utf8.size(), NULL);
}

static PyObject* PDF_read(PDF* self, PyObject* args, PyObject* kwds) {
    int page_number;
    static char* kwlist[] = {(char*)"page_number", NULL};

    if (self->doc == NULL) {
        return PyErr_Format(PdftotextError, "No document to read");
    }
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "i", kwlist, &page_number)) {
        return NULL;
    }
    if (page_number < 1 || page_number > self->page_count) {
        return PyErr_Format(
            PdftotextError, "Invalid page number: %i", page_number);
    }
    return PDF_read_page(self, page_number);
}

static PyObject* PDF_read_all(PDF* self) {
    const poppler::page* page;
    std::vector<char> page_utf8;
    std::vector<char> doc_utf8;

    if (self->doc == NULL) {
        return PyErr_Format(PdftotextError, "No document to read");
    }
    for (int i = 0; i < self->page_count; i++) {
        if (i != 0) {
            doc_utf8.push_back('\n');
            doc_utf8.push_back('\n');
        }
        page = self->doc->create_page(i);
        if (page == NULL) {
            return PyErr_Format(PdftotextError, "Poppler error creating page");
        }
        page_utf8 = page->text().to_utf8();
        delete page;
        doc_utf8.insert(doc_utf8.end(), page_utf8.begin(), page_utf8.end());
    }
    return PyUnicode_DecodeUTF8(doc_utf8.data(), doc_utf8.size(), NULL);
}

static PyMethodDef PDF_methods[] = {
    {
        "read",
        (PyCFunction)PDF_read,
        METH_VARARGS | METH_KEYWORDS,
        "Extract text from the given page number.",
    },
    {
        "read_all",
        (PyCFunction)PDF_read_all,
        METH_NOARGS,
        "Extract all text from the document, joining pages with \"\\n\\n\".",
    },
    {NULL},  // Sentinel
};

static PyTypeObject PDFType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pdftotext.PDF",                           // tp_name
    sizeof(PDF),                               // tp_basicsize
    0,                                         // tp_itemsize
    (destructor)PDF_dealloc,                   // tp_dealloc
    0,                                         // tp_print
    0,                                         // tp_getattr
    0,                                         // tp_setattr
    0,                                         // tp_reserved
    0,                                         // tp_repr
    0,                                         // tp_as_number
    0,                                         // tp_as_sequence
    0,                                         // tp_as_mapping
    0,                                         // tp_hash
    0,                                         // tp_call
    0,                                         // tp_str
    0,                                         // tp_getattro
    0,                                         // tp_setattro
    0,                                         // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,  // tp_flags
    "PDF document.",                           // tp_doc
    0,                                         // tp_traverse
    0,                                         // tp_clear
    0,                                         // tp_richcompare
    0,                                         // tp_weaklistoffset
    0,                                         // tp_iter
    0,                                         // tp_iternext
    PDF_methods,                               // tp_methods
    PDF_members,                               // tp_members
    0,                                         // tp_getset
    0,                                         // tp_base
    0,                                         // tp_dict
    0,                                         // tp_descr_get
    0,                                         // tp_descr_set
    0,                                         // tp_dictoffset
    (initproc)PDF_init,                        // tp_init
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
static PyMethodDef module_methods[] = {
    {NULL},  // Sentinel
};

PyMODINIT_FUNC initpdftotext() {
    PyObject* module;

    PDFType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&PDFType) < 0) {
        return;
    }

    module = Py_InitModule3(
        "pdftotext", module_methods, "Simple PDF text extraction.");
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
