const fs = require('fs');
const express = require('express')
const { spawn } = require('child_process');
const cors = require('cors');
const app = express()

const multer = require('multer')
const upload = multer();
const path = require('path');

const port = 5000

app.use(cors())

// for parsing application/json
app.use(express.json());

// for parsing application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// for parsing multipart/form-data
app.use(upload.array());

app.use('/tiffs', express.static(process.cwd() + '/tiffs'))

app.post('/', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['geoprocess.py', req.body.density, req.body.estiasi, req.body.parking, req.body.pois, req.body.transport, req.body.uid]);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe raster max value from python script ...', data);
        dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend);
    });
})

app.post('/delete', (req, res) => {

    let dir = `./tiffs/${req.body.id}`

    if (fs.existsSync(dir)) {
        fs.rm(dir, { recursive: true }, (err) => {
            if (err) {
                throw err;
            }

            console.log(`${dir} is deleted!`);
        });
    }

})


//route to save geotiffs

app.get('/tiffs', (req, res) => {

})


app.listen(port, () => console.log(`App listening on port 
   ${port}!`))