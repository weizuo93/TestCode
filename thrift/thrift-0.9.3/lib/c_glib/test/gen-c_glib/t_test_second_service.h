/**
 * Autogenerated by Thrift Compiler (0.9.3)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#ifndef T_TEST_SECOND_SERVICE_H
#define T_TEST_SECOND_SERVICE_H

#include <thrift/c_glib/processor/thrift_dispatch_processor.h>

#include "t_test_thrift_test_types.h"

/* SecondService service interface */
typedef struct _TTestSecondServiceIf TTestSecondServiceIf;  /* dummy object */

struct _TTestSecondServiceIfInterface
{
  GTypeInterface parent;

  gboolean (*blah_blah) (TTestSecondServiceIf *iface, GError **error);
  gboolean (*secondtest_string) (TTestSecondServiceIf *iface, gchar ** _return, const gchar * thing, GError **error);
};
typedef struct _TTestSecondServiceIfInterface TTestSecondServiceIfInterface;

GType t_test_second_service_if_get_type (void);
#define T_TEST_TYPE_SECOND_SERVICE_IF (t_test_second_service_if_get_type())
#define T_TEST_SECOND_SERVICE_IF(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), T_TEST_TYPE_SECOND_SERVICE_IF, TTestSecondServiceIf))
#define T_TEST_IS_SECOND_SERVICE_IF(obj) (G_TYPE_CHECK_INSTANCE_TYPE ((obj), T_TEST_TYPE_SECOND_SERVICE_IF))
#define T_TEST_SECOND_SERVICE_IF_GET_INTERFACE(inst) (G_TYPE_INSTANCE_GET_INTERFACE ((inst), T_TEST_TYPE_SECOND_SERVICE_IF, TTestSecondServiceIfInterface))

gboolean t_test_second_service_if_blah_blah (TTestSecondServiceIf *iface, GError **error);
gboolean t_test_second_service_if_secondtest_string (TTestSecondServiceIf *iface, gchar ** _return, const gchar * thing, GError **error);

/* SecondService service client */
struct _TTestSecondServiceClient
{
  GObject parent;

  ThriftProtocol *input_protocol;
  ThriftProtocol *output_protocol;
};
typedef struct _TTestSecondServiceClient TTestSecondServiceClient;

struct _TTestSecondServiceClientClass
{
  GObjectClass parent;
};
typedef struct _TTestSecondServiceClientClass TTestSecondServiceClientClass;

GType t_test_second_service_client_get_type (void);
#define T_TEST_TYPE_SECOND_SERVICE_CLIENT (t_test_second_service_client_get_type())
#define T_TEST_SECOND_SERVICE_CLIENT(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), T_TEST_TYPE_SECOND_SERVICE_CLIENT, TTestSecondServiceClient))
#define T_TEST_SECOND_SERVICE_CLIENT_CLASS(c) (G_TYPE_CHECK_CLASS_CAST ((c), T_TEST_TYPE_SECOND_SERVICE_CLIENT, TTestSecondServiceClientClass))
#define T_TEST_SECOND_SERVICE_IS_CLIENT(obj) (G_TYPE_CHECK_INSTANCE_TYPE ((obj), T_TEST_TYPE_SECOND_SERVICE_CLIENT))
#define T_TEST_SECOND_SERVICE_IS_CLIENT_CLASS(c) (G_TYPE_CHECK_CLASS_TYPE ((c), T_TEST_TYPE_SECOND_SERVICE_CLIENT))
#define T_TEST_SECOND_SERVICE_CLIENT_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), T_TEST_TYPE_SECOND_SERVICE_CLIENT, TTestSecondServiceClientClass))

gboolean t_test_second_service_client_blah_blah (TTestSecondServiceIf * iface, GError ** error);
gboolean t_test_second_service_client_send_blah_blah (TTestSecondServiceIf * iface, GError ** error);
gboolean t_test_second_service_client_recv_blah_blah (TTestSecondServiceIf * iface, GError ** error);
gboolean t_test_second_service_client_secondtest_string (TTestSecondServiceIf * iface, gchar ** _return, const gchar * thing, GError ** error);
gboolean t_test_second_service_client_send_secondtest_string (TTestSecondServiceIf * iface, const gchar * thing, GError ** error);
gboolean t_test_second_service_client_recv_secondtest_string (TTestSecondServiceIf * iface, gchar ** _return, GError ** error);
void second_service_client_set_property (GObject *object, guint property_id, const GValue *value, GParamSpec *pspec);
void second_service_client_get_property (GObject *object, guint property_id, GValue *value, GParamSpec *pspec);

/* SecondService handler (abstract base class) */
struct _TTestSecondServiceHandler
{
  GObject parent;
};
typedef struct _TTestSecondServiceHandler TTestSecondServiceHandler;

struct _TTestSecondServiceHandlerClass
{
  GObjectClass parent;

  gboolean (*blah_blah) (TTestSecondServiceIf *iface, GError **error);
  gboolean (*secondtest_string) (TTestSecondServiceIf *iface, gchar ** _return, const gchar * thing, GError **error);
};
typedef struct _TTestSecondServiceHandlerClass TTestSecondServiceHandlerClass;

GType t_test_second_service_handler_get_type (void);
#define T_TEST_TYPE_SECOND_SERVICE_HANDLER (t_test_second_service_handler_get_type())
#define T_TEST_SECOND_SERVICE_HANDLER(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), T_TEST_TYPE_SECOND_SERVICE_HANDLER, TTestSecondServiceHandler))
#define T_TEST_IS_SECOND_SERVICE_HANDLER(obj) (G_TYPE_CHECK_INSTANCE_TYPE ((obj), T_TEST_TYPE_SECOND_SERVICE_HANDLER))
#define T_TEST_SECOND_SERVICE_HANDLER_CLASS(c) (G_TYPE_CHECK_CLASS_CAST ((c), T_TEST_TYPE_SECOND_SERVICE_HANDLER, TTestSecondServiceHandlerClass))
#define T_TEST_IS_SECOND_SERVICE_HANDLER_CLASS(c) (G_TYPE_CHECK_CLASS_TYPE ((c), T_TEST_TYPE_SECOND_SERVICE_HANDLER))
#define T_TEST_SECOND_SERVICE_HANDLER_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), T_TEST_TYPE_SECOND_SERVICE_HANDLER, TTestSecondServiceHandlerClass))

gboolean t_test_second_service_handler_blah_blah (TTestSecondServiceIf *iface, GError **error);
gboolean t_test_second_service_handler_secondtest_string (TTestSecondServiceIf *iface, gchar ** _return, const gchar * thing, GError **error);

/* SecondService processor */
struct _TTestSecondServiceProcessor
{
  ThriftDispatchProcessor parent;

  /* protected */
  TTestSecondServiceHandler *handler;
  GHashTable *process_map;
};
typedef struct _TTestSecondServiceProcessor TTestSecondServiceProcessor;

struct _TTestSecondServiceProcessorClass
{
  ThriftDispatchProcessorClass parent;

  /* protected */
  gboolean (*dispatch_call) (ThriftDispatchProcessor *processor,
                             ThriftProtocol *in,
                             ThriftProtocol *out,
                             gchar *fname,
                             gint32 seqid,
                             GError **error);
};
typedef struct _TTestSecondServiceProcessorClass TTestSecondServiceProcessorClass;

GType t_test_second_service_processor_get_type (void);
#define T_TEST_TYPE_SECOND_SERVICE_PROCESSOR (t_test_second_service_processor_get_type())
#define T_TEST_SECOND_SERVICE_PROCESSOR(obj) (G_TYPE_CHECK_INSTANCE_CAST ((obj), T_TEST_TYPE_SECOND_SERVICE_PROCESSOR, TTestSecondServiceProcessor))
#define T_TEST_IS_SECOND_SERVICE_PROCESSOR(obj) (G_TYPE_CHECK_INSTANCE_TYPE ((obj), T_TEST_TYPE_SECOND_SERVICE_PROCESSOR))
#define T_TEST_SECOND_SERVICE_PROCESSOR_CLASS(c) (G_TYPE_CHECK_CLASS_CAST ((c), T_TEST_TYPE_SECOND_SERVICE_PROCESSOR, TTestSecondServiceProcessorClass))
#define T_TEST_IS_SECOND_SERVICE_PROCESSOR_CLASS(c) (G_TYPE_CHECK_CLASS_TYPE ((c), T_TEST_TYPE_SECOND_SERVICE_PROCESSOR))
#define T_TEST_SECOND_SERVICE_PROCESSOR_GET_CLASS(obj) (G_TYPE_INSTANCE_GET_CLASS ((obj), T_TEST_TYPE_SECOND_SERVICE_PROCESSOR, TTestSecondServiceProcessorClass))

#endif /* T_TEST_SECOND_SERVICE_H */
