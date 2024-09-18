document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('audioForm');
    const statusDiv = document.getElementById('status');
    const loaderDiv = document.getElementById('loader');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form behavior

        const fileInput = document.getElementById('file');
        const file = fileInput.files[0];

        if (!file) {
            statusDiv.textContent = 'Por favor, selecione um arquivo de áudio.';
            return;
        }

        // Create a FileReader to read the file as ArrayBuffer
        const reader = new FileReader();

        reader.onload = async (e) => {
            const arrayBuffer = e.target.result;

            loaderDiv.style.display = 'block'; // Show the loader
            statusDiv.textContent = ''; // Clear previous status

            try {
                const response = await fetch('https://f6du96p34c.execute-api.us-east-1.amazonaws.com/v1/send-songs', {
                    method: 'POST',
                    body: arrayBuffer,
                    headers: {
                        'Content-Type': 'audio/mpeg', // Ensure this matches the expected MIME type
                    },
                });

                const result = await response.text(); // Get the response text

                if (response.ok) {
                    statusDiv.textContent = 'Áudio enviado com sucesso!';
                } else {
                    statusDiv.textContent = `Falha ao enviar o áudio. Código: ${response.status}. Mensagem: ${result}`;
                }
            } catch (error) {
                console.error('Erro ao enviar o áudio:', error); // Log the error
                statusDiv.textContent = `Ocorreu um erro ao enviar o áudio: ${error.message}`;
            } finally {
                loaderDiv.style.display = 'none'; // Hide the loader
            }
        };

        reader.onerror = (error) => {
            console.error('Erro ao ler o arquivo:', error); // Log the error
            statusDiv.textContent = `Erro ao ler o arquivo: ${error.message}`;
        };

        reader.readAsArrayBuffer(file); // Read the file as ArrayBuffer
    });
});
