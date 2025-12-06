@echo off
echo ========================================
echo ISP Payment Recovery System - Docker
echo ========================================
echo.
echo Starting application with Docker...
echo.

docker-compose up -d

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo Application started successfully!
    echo ========================================
    echo.
    echo Access at: http://localhost:5000
    echo.
    echo To view logs: docker-compose logs -f
    echo To stop: docker-compose down
    echo.
    pause
) else (
    echo.
    echo Error starting Docker container.
    echo Make sure Docker Desktop is running.
    echo.
    pause
)

