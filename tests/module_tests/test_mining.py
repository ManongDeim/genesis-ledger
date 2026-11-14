def test_mining_workflow(client_app):
    #Queue a dummy transaction
    add_res = client_app.post('/api/add', json={
        "sender": "Aira",
        "receiver": "Deim",
        "amount": 50
    })
    assert add_res.status_code == 200
    
    #Verify it is in mempool
    tx_res_1 = client_app.get('/api/transactions')
    assert len(tx_res_1.get_json()["pending"]) == 1
    assert len(tx_res_1.get_json()["completed"]) == 0
    
    #Mine the block
    mine_res = client_app.post('/api/mine')
    assert mine_res.status_code == 200
    assert "block_id" in mine_res.json
    
    #Verify mempool is cleared and ledger is updated
    tx_res_2 = client_app.get('/api/transactions')
    assert len(tx_res_2.get_json()["pending"]) == 0
    assert len(tx_res_2.get_json()["completed"]) == 1
    assert "Block-" in tx_res_2.get_json()["completed"][0]["block_id"]