function query(queryString, onResponse) {
    const xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.open("POST", '/graphiql/');
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Accept", "application/json");

    xhr.onload = function () {
        onResponse(xhr.response.data);
    };

    xhr.send(JSON.stringify({query: queryString}));
}

