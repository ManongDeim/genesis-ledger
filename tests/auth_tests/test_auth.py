def test_auth_workflow(client_app):
    # Registration test
    reg_res = client_app.post('/api/register', json={
        "username": "testuser",
        "email":"testuser@example.com",
        "password": "testpassword"
    })
    assert reg_res.status_code == 201
    
    #Duplicate Username Block test
    dup_res =client_app.post('/api/register', json={
        "username": "testuser",
        "email":"newemail@example.com",
        "password": "newpassword"
    })
    assert dup_res.status_code == 400
    assert "Username is already taken." in dup_res.get_json()["message"]
    
    #Test successful login
    login_res = client_app.post('/api/login', json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert login_res.status_code == 200
    assert "token" in login_res.get_json()