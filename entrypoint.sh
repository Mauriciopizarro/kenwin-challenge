#!/bin/sh
uvicorn starter:app --host 0.0.0.0 --port $FAST_API_PORT --reload ;