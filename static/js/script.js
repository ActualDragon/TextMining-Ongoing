document.addEventListener("DOMContentLoaded",
  function (event) {
    const fileInput = document.getElementById('myfile');
    fileInput.onchange = () => {
        const file = document.getElementById("myfile").value;
        console.log(file)
        document.getElementById("submit_file").addEventListener("click", SendFile(file));
    }

    function SendFile(file) {
        const requestOptions = {
            headers: {
                "Content-Type": file.contentType, // This way, the Content-Type value in the header will always match the content type of the file
            },
            mode: "no-cors",
            method: "POST",
            files: file,
        };
        console.log(requestOptions);

        fetch("http://localhost:5000/index", requestOptions).then(
            (response) => {
                console.log(response.data);
            }
        );

    }
  }
)




