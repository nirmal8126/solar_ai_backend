from fastapi.responses import JSONResponse

@router.post("/login")
def login(data: LoginSchema):
    token = create_access_token(data.email)

    response = JSONResponse({"message": "Login success"})
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )
    return response
