argv = require 'yargs'
    .argv
gulp = require 'gulp'
path = require 'path'
rename = require 'gulp-rename'
template = require 'gulp-template'


# Helpers and config

productionMode = argv.production

outputDirectory = path.join __dirname, 'deploy'



gulp.task 'default', ['createsettings'], ->


gulp.task 'createsettings', ->
    secretKey = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    for i in [1..50]
        randomnumber = Math.floor Math.random() * chars.length
        secretKey += chars[randomnumber]
    gulp.src path.join __dirname, 'NotarTH', 'default_settings.py'
    .pipe template
        secretKey: secretKey
    .pipe rename 'settings.py'
    .pipe gulp.dest outputDirectory
