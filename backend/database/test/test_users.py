from database.crud.users import create_user_and_commit, read_users, read_hashed_password, update_hashed_password


def test_create_and_read_users(
        db_session,
        users,
):
    for item in users:
        create_user_and_commit(
            session=db_session,
            last_name=item["last_name"],
            first_name=item["first_name"],
            middle_name=item["middle_name"],
            hashed_password=item["hashed_password"],
        )

    result = read_users(session=db_session)
    assert len(result) == len(users)
    for index, item in enumerate(users):
        assert result[index].last_name == item["last_name"]
        assert result[index].first_name == item["first_name"]
        assert result[index].middle_name == item["middle_name"]
        assert result[index].hashed_password == item["hashed_password"]


def test_create_user_and_read_hashed_password(db_session, users):
    hashed_password = "top_secret"
    for index, item in enumerate(users):
        create_user_and_commit(
            session=db_session,
            last_name=item["last_name"],
            first_name=item["first_name"],
            middle_name=item["middle_name"],
            # create unique password for all mock users
            hashed_password=f"{hashed_password} {index}",
        )

    result_hashed_pass = read_hashed_password(
        session=db_session,
        user_id=1,
    )
    print(result_hashed_pass)
    assert result_hashed_pass == f"{hashed_password} 0"


def test_create_user_and_update_hashed_password(db_session, users):
    hashed_password = "top_secret"
    update_password = "update_top_secret"
    create_user_and_commit(
        session=db_session,
        last_name=users[0]["last_name"],
        first_name=users[0]["first_name"],
        middle_name=users[0]["middle_name"],
        hashed_password=hashed_password,
    )

    update_hashed_password(
        session=db_session,
        user_id=1,
        new_hashed_password=update_password
    )

    result_hashed_pass = read_hashed_password(
        session=db_session,
        user_id=1,
    )
    print(result_hashed_pass)
    assert result_hashed_pass == update_password
