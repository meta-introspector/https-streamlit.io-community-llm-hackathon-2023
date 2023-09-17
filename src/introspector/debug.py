
##inject code

#if not os.path.exists(target):
#    os.mkdir(target)

#ctx =streamlit.runtime.scriptrunner.script_runner.get_script_run_ctx()

# st.write("CTX",ctx)
# st.write("CTX",str(ctx))
# st.write("Sess",dir(ctx))
# for x in dir(ctx):
#     st.write("DEBUG",x,getattr(ctx,x,"None"))

    
# ctxScriptRunContextScriptRunContext(session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _enqueue=<bound method ScriptRunner._enqueue_forward_msg of ScriptRunner(_session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _main_script_path='./src/streamlit_app.py', _uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore...
# A context object that contains data for a "script run" - that is,
# data that's scoped to a single ScriptRunner execution (and therefore also
# scoped to a single connected "session").

# ScriptRunContext is used internally by virtually every `st.foo()` function.
# It is accessed only from the script thread that's created by ScriptRunner.

# Streamlit code typically retrieves the active ScriptRunContext via the
# `get_script_run_ctx` function.
# command_tracking_deactivatedbool	True
# cursorsdict	{}
# dg_stacklist	[]
# form_ids_this_runset	set()
# gather_usage_statsbool	True
# page_script_hashstr	'04d9c6d3425fdb18dfa2143151c97767'
# query_stringstr	''
# session_idstr	'6ab6368d-3bf6-492e-a2d0-d8d3a5733e71'
# session_stateSafeSessionState	Thread-safe wrapper around SessionState.
# tracked_commandslist	[name: "write" args { k: "1" t: "streamlit.runtime.scriptrunner.script_run_context.ScriptRunContext" p: 1 } ]
# tracked_commands_counterCounter	Counter({'write': 1})
# uploaded_file_mgrMemoryUploadedFileManager	MemoryUploadedFileManager(endpoint='/_stcore/upload_file')
# user_infodict	{'email': 'test@localhost.com'}
# widget_ids_this_runset	set()
# widget_user_keys_this_runset	set()
# enqueuemethod	Enqueue a ForwardMsg for this context's session.
# on_script_startmethod	No docs available
# resetmethod	No docs available
# ScriptRunContext(session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _enqueue=<bound method ScriptRunner._enqueue_forward_msg of ScriptRunner(_session_id='6ab6368d-3bf6-492e-a2d0-d8d3a5733e71', _main_script_path='./src/streamlit_app.py', _uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore/upload_file'), _script_cache=<streamlit.runtime.scriptrunner.script_cache.ScriptCache object at 0x7f305f154d90>, _user_info={'email': 'test@localhost.com'}, _client_state=, _session_state=<streamlit.runtime.state.safe_session_state.SafeSessionState object at 0x7f305cc78670>, _requests=<streamlit.runtime.scriptrunner.script_requests.ScriptRequests object at 0x7f304dc0b2e0>, on_event=<blinker.base.Signal object at 0x7f304dc0ba30>, _execing=True, _script_thread=<Thread(ScriptRunner.scriptThread, started 139845467305536)>)>, query_string='', session_state=<streamlit.runtime.state.safe_session_state.SafeSessionState object at 0x7f305cc78670>, uploaded_file_mgr=MemoryUploadedFileManager(endpoint='/_stcore/upload_file'), page_script_hash='04d9c6d3425fdb18dfa2143151c97767', user_info={'email': 'test@localhost.com'}, gather_usage_stats=True, command_tracking_deactivated=False, tracked_commands=[name: "write" args { k: "1" t: "streamlit.runtime.scriptrunner.script_run_context.ScriptRunContext" p: 1 } time: 5345 ], tracked_commands_counter=Counter({'write': 1}), _set_page_config_allowed=False, _has_script_started=True, widget_ids_this_run=set(), widget_user_keys_this_run=set(), form_ids_this_run=set(), cursors={0: RunningCursor(_parent_path=(), _index=1)}, dg_stack=[])
                                                                                                                                                                                                                                                                                                             
#st.write("Sess STate",ctx.session_state._state)
#st.write("Sess STate",dir(ctx.session_state._state))
#st.write("Sess",dir(ctx.session_state))


values = {}


#st.write("current",tornado.ioloop.IOLoop.current())

#import pdb
#pdb.set_trace()

# for x in inspect.stack():
#     st.write("CALLBACK",str(x))
#     #st.write(dir(x))
#     st.write("CALLBACK1",x.frame)
#     st.write("CALLBACK2",x.frame.f_globals)
#     st.write("CALLBACK3",x.code_context)
            
#for line in traceback.format_stack():
#    st.write(line.strip())
#    st.write(line)
        
_io_loops= {}
_io_loop = tornado.ioloop.IOLoop.current()
#st.write("current",type(_io_loop).__name__)
if _io_loop not in _io_loops:
    _io_loops[_io_loop] = True
    #st.write("started ")

    asyncio_loop = _io_loop.asyncio_loop  # type: ignore

    #st.write("asyncio_loop ",asyncio_loop)
    tasks = asyncio.all_tasks(asyncio_loop)  # type: ignore

    asyncio_loop.set_debug(True)
    #for x in dir(asyncio_loop):
    #    st.write(x)
    #st.write("asyncio_loop tasks", tasks)
#if hasattr(asyncio, "all_tasks"):  # py37

#        else:
#           tasks = asyncio.Task.all_tasks(asyncio_loop)


    #modify_times = {}  # type: Dict[str, float]
    #callback = functools.partial(_reload_on_update, modify_times)
    #scheduler = ioloop.PeriodicCallback(callback, check_time)
    #scheduler.start()


# for x in list(globals()):
#     v = globals()[x]

#     if isinstance(v, types.ModuleType):
#         values[x] = globals()[x]
    

st.write("server")
#st.dataframe(dir(streamlit.web.server.server))
for module in values:
    st.write(module)
    #st.write(help(module))
    #for x in values[module]:
    #    v = values[module][x]
    #    st.write(module,x,v)
    #st.dataframe(dir(module))

#st.dataframe(dir(streamlit))

