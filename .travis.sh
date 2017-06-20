function generate()
{
    cmake -G "Unix Makefiles"
}

generate && make -j4
