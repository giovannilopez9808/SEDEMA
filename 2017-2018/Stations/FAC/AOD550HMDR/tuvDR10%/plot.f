        program plot
        character file*6
        real ozono,a
        open(1,file="datos.txt")
        open(2,file="plot.gpl")
        write(2,*) "set term png"
        read(1,*) n
        do i=1,n
        read(1,*) file,a,a,a,ozono
        if(ozono.ne.0) then
        write(2,*) "set output '",file,".png'"
        write(2,*) "set xlabel 'Local hour'"
        write(2,*) "set ylabel 'Irradiance solar'"
        write(2,*) "plot '",file,"med.txt' title 'Medicion' with lp,'"
     &  ,file,"mod.txt' title 'Modelo TUV' with lp"
        end if
        end do
        close(2)
        close(1)
        end program
