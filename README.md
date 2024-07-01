# PG_FINAL_PROJECT

<div style="text-align: center;">

![image](https://github.com/Cris272500/PG_Final_Project/assets/113935131/91e15ea8-df38-4e7f-b1e1-738755ea70bf)


</div>

## PROYECTO FINAL DE PROGRAMACIÓN GRÁFICA

<h3 style="text-decoration: underline;">Integrantes</h1>

1. Espinoza Ruíz Norman Alfonso 2022-0480U
2. Ruiz Torres Josué Israel 2022-0357U
3. Quintana Cerna Cristopher David 2022-0301U
4. Duarte Lacayo Josué Gabriel 2022-0409U
   
<h3 style="text-decoration: underline;">Grupo</h3>

3T2-CO

<h3 style="text-decoration: underline;">Docente</h3>

Ing. Danny Chávez
___

<div style="text-align: center;"> <h2>Resumen del proyecto</h2> </div>
Nuestro equipo ha desarrollado un entorno virtual 3D que permite a los usuarios sumergirse en un campo de fútbol, específicamente en el estadio del FC Barcelona, ubicado en España, Europa. Con este proyecto, buscamos superar las barreras de distancia y económicas, permitiendo que cualquier aficionado de este equipo pueda experimentar de manera inmersiva el ambiente del estadio del FC Barcelona.

<div style="text-align: center;"> <h2>Tecnologías utilizadas</h2> </div>
Para el desarrollo de este proyecto, hemos empleado una variedad de tecnologías, incluyendo lenguajes de programación, control de versiones y software de modelado 3D.

1. **Python**: Elegimos Python como el lenguaje de programación principal para el desarrollo del proyecto. Utilizamos módulos como **moderngl, pygame, PYWAVE y pyopengl**.

	- **Moderngl:** Para el renderizado moderno de gráficos 3D utilizando opengl.

	- **Pygame**: Para el manejo de eventos y la integración de elementos multimedia.

	- **PYWAVE:** Para la simulación de ondas y efectos sonoros en el entorno virtual

	- **Pyopengl:** Para la integración de gráficos 3D utilizando opengl.

2. **Blender:** Blender fue utilizado para probar y modificar los modelos 3D.

3. **Git**: Utilizamos Git para el control de versiones y para facilitar el desarrollo colaborativo del proyecto.

<div style="text-align: center;"> <h2>Instalaciones</h2> </div>
Anteriormente, se explico los distintos módulos que usamos en este proyecto, para poder hacer uso de estos, realizaremos las siguientes configuraciones

1. Tener instalado Python
	Para poder verificar que tenemos instalado correctamente instalado python, abrimos la CMD y ejecutamos el siguiente comando
	**`python --version`**
	en la terminal, debería de aparecer que versión de Python tienes instalada, sino la tienes instalada, no se podrá ejecutar el proyecto, para mayor información sobre su instalación puedes seguir el siguiente tutorial que explica cómo instalarlo
	<div align="center">
        <a href="https://youtu.be/yivyNCtVVDk?si=3PrPei8bh1wLwRFT">
            <img src="https://img.youtube.com/vi/yivyNCtVVDk/0.jpg" alt="Video de YouTube" style="width:560px;height:315px;">
        </a>
    </div>

---
2. Crear un entorno virtual
	Para hacer uso de los módulos usados en este proyecto, es necesario crear un entorno virtual para que de ésta manera se puedan instalar correctamente con sus respectivas versiones, para ello usamos
	**`python -m venv env`**
	esto lo que hará es crear una carpeta llamada `env` en la cual tendrá todos los módulos necesarios para este proyecto
---
3. Activar el entorno virtual
	Una vez creado, ejecutaremos el siguiente comando para poder activarlo e instalar los módulos
	`.\env\Scripts\activate`
	luego, para tener los módulos con las mismas versiones utilizadas en el proyecto usamos el comando para instalar todos los módulos que utilizamos con sus versiones
	`pip install -r requirements.txt`
---
4. Ejecución del proyecto
	Cuando hallamos completado los anteriores pasos, ejecutamos `cd Project-Origin-Version 1.0` y dentro de esta carpeta debería de aparecer una estructura como ésta
	![image](https://github.com/Cris272500/PG_Final_Project/assets/113935131/b1e65d15-9e6a-4e4e-a211-bf9d1429c4cb)
	y ejecutamos `python UI.py` de  ésta manera estaríamos ejecutando el proyecto