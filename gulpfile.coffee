argv = require 'yargs'
    .argv
cleanCSS = require 'gulp-cleancss'
concat = require 'gulp-concat'
gulp = require 'gulp'
gulpif = require 'gulp-if'
mainBowerFiles = require 'main-bower-files'
path = require 'path'
rename = require 'gulp-rename'
template = require 'gulp-template'
uglify = require 'gulp-uglify'


# Helpers and config

productionMode = argv.production

outputDirectory = path.join __dirname, 'NotarDeploy'

staticDirectory = path.join outputDirectory, 'static'


# Gulp default task

gulp.task 'default', ['createsettings', 'createwsgifile', 'css', 'js'], ->


# Django settings file

gulp.task 'createsettings', ->
    secretKey = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    for i in [1..50]
        randomnumber = Math.floor Math.random() * chars.length
        secretKey += chars[randomnumber]
    gulp.src path.join __dirname, 'Notar', 'default_settings.py'
    .pipe template
        outputDirectoryBaseName: path.basename outputDirectory
        secretKey: secretKey
    .pipe rename 'settings.py'
    .pipe gulp.dest outputDirectory

gulp.task 'createwsgifile', ->
    gulp.src path.join __dirname, 'Notar', 'default_wsgi.py'
    .pipe template
        outputDirectory: outputDirectory
        outputDirectoryBaseName: path.basename outputDirectory
    .pipe rename 'wsgi.py'
    .pipe gulp.dest outputDirectory


# CSS and font files

gulp.task 'css', ['css-custom', 'css-libs', 'fonts-libs', 'maps-libs'], ->

gulp.task 'css-custom', ->

gulp.task 'css-libs', ->
    gulp.src mainBowerFiles
        filter: /\.css$/
    .pipe concat 'notar-libs.css'
    .pipe gulpif productionMode, cleanCSS
        compatibility: 'ie8'
    .pipe gulp.dest path.join staticDirectory, 'css'

gulp.task 'fonts-libs', ->
    gulp.src mainBowerFiles
        filter: /\.(eot)|(svg)|(ttf)|(woff)|(woff2)$/
    .pipe gulp.dest path.join staticDirectory, 'fonts'

gulp.task 'maps-libs', ->
    gulp.src mainBowerFiles
        filter: /\.map$/
    .pipe gulp.dest path.join staticDirectory, 'css'


# JavaScript files

gulp.task 'js', ['coffee', 'js-custom', 'js-libs'], ->

gulp.task 'coffee', ->

gulp.task 'js-custom', ->

gulp.task 'js-libs', ->
    isntSpecialFile = (file) ->
        name = path.basename file.path
        name isnt 'html5shiv.js' and name isnt 'respond.src.js'
    gulp.src mainBowerFiles
        filter: /\.js$/
    .pipe gulpif isntSpecialFile, concat 'notar-libs.js'
    .pipe gulpif productionMode, uglify()
    .pipe gulp.dest path.join staticDirectory, 'js'
