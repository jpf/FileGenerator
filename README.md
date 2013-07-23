This is a sorta-StringIO-like file-like object where writes go into a Queue and reads are done via a generator.

I wrote this to allow myself to stream a file as the file was being written.

I'm not sure if this code will be useful to anybody other than me. So I'm posting it to GitHub Just In Case.

Here is how to use FileGenerator, with an example of how I actually use it to stream a WAV file as the WAV file is being written.

    def live_martin_m2_renderer(image):
        # Create a FileGenerator
        generator = FileGenerator()
        slowscan = MartinM2Generator(image, 48000, 16)
    	# Pass the FileGenerator to a thread that will start writing to the FileGenerator
        MartinM2GeneratorWorker(slowscan, generator).start()

        # Give the read_generator() to Flask, to stream the data as it is being written to the "file"
        rv = Response(generator.read_generator(), mimetype='audio/wav')
        rv.headers['Content-Length'] = 5661190
        return rv