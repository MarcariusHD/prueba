import os
import shutil
import random
import tkinter as tk

from tkinter import filedialog, messagebox


# ============================================================
# CONFIGURACIÓN
# ============================================================

TRAIN_RATIO = 0.80
VAL_RATIO = 0.15
TEST_RATIO = 0.05

RANDOM_SEED = 42


# ============================================================
# CLASE PRINCIPAL
# ============================================================

class DatasetPreparator:

    def __init__(self, root):

        self.root = root

        self.root.title("Preparador de Dataset YOLO")
        self.root.geometry("850x650")
        self.root.configure(bg="#111827")

        self.dataset_dir = None
        self.labels_dir = None
        self.output_dir = None
        self.class_name = None

        self.build_interface()


    # ========================================================
    # INTERFAZ
    # ========================================================

    def build_interface(self):

        title = tk.Label(
            self.root,
            text="PREPARADOR DE DATASET YOLO",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#111827"
        )

        title.pack(pady=(25, 5))


        subtitle = tk.Label(
            self.root,
            text="Convierte tus imágenes y anotaciones en un dataset listo para entrenar",
            font=("Segoe UI", 11),
            fg="#9ca3af",
            bg="#111827"
        )

        subtitle.pack(pady=(0, 25))


        # ----------------------------------------------------
        # BOTÓN SELECCIONAR DATASET
        # ----------------------------------------------------

        self.btn_dataset = tk.Button(
            self.root,
            text="1. SELECCIONAR CARPETA DATASET",
            command=self.select_dataset,
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )

        self.btn_dataset.pack(pady=8)


        # ----------------------------------------------------
        # BOTÓN SELECCIONAR LABELS
        # ----------------------------------------------------

        self.btn_labels = tk.Button(
            self.root,
            text="2. SELECCIONAR CARPETA LABELS",
            command=self.select_labels,
            font=("Segoe UI", 12, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            padx=20,
            pady=12,
            relief="flat",
            cursor="hand2"
        )

        self.btn_labels.pack(pady=8)


        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

        self.info_label = tk.Label(
            self.root,
            text="Todavía no se ha seleccionado ninguna carpeta.",
            font=("Segoe UI", 11),
            fg="#d1d5db",
            bg="#111827",
            justify="left"
        )

        self.info_label.pack(
            pady=20,
            padx=30
        )


        # ----------------------------------------------------
        # BOTÓN PREPARAR
        # ----------------------------------------------------

        self.btn_prepare = tk.Button(
            self.root,
            text="3. PREPARAR DATASET YOLO",
            command=self.prepare_dataset,
            font=("Segoe UI", 14, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            padx=25,
            pady=15,
            relief="flat",
            cursor="hand2"
        )

        self.btn_prepare.pack(pady=15)


        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        self.log = tk.Text(
            self.root,
            height=18,
            width=90,
            bg="#020617",
            fg="#d1d5db",
            insertbackground="white",
            font=("Consolas", 10)
        )

        self.log.pack(
            padx=25,
            pady=15,
            fill="both",
            expand=True
        )


    # ========================================================
    # LOG
    # ========================================================

    def write_log(self, text):

        self.log.insert(
            tk.END,
            text + "\n"
        )

        self.log.see(tk.END)

        self.root.update_idletasks()


    # ========================================================
    # SELECCIONAR DATASET
    # ========================================================

    def select_dataset(self):

        folder = filedialog.askdirectory(
            title="Selecciona la carpeta dataset"
        )

        if not folder:
            return

        self.dataset_dir = folder

        self.write_log(
            f"Dataset seleccionado: {folder}"
        )

        self.update_info()


    # ========================================================
    # SELECCIONAR LABELS
    # ========================================================

    def select_labels(self):

        folder = filedialog.askdirectory(
            title="Selecciona la carpeta labels"
        )

        if not folder:
            return

        self.labels_dir = folder

        self.write_log(
            f"Labels seleccionados: {folder}"
        )

        self.update_info()


    # ========================================================
    # ACTUALIZAR INFORMACIÓN
    # ========================================================

    def update_info(self):

        texto = ""

        if self.dataset_dir:

            texto += (
                f"📁 DATASET:\n"
                f"{self.dataset_dir}\n\n"
            )

        if self.labels_dir:

            texto += (
                f"🏷 LABELS:\n"
                f"{self.labels_dir}\n"
            )

        if not texto:

            texto = "Todavía no se ha seleccionado ninguna carpeta."

        self.info_label.config(
            text=texto
        )


    # ========================================================
    # DETECTAR CLASE
    # ========================================================

    def detect_class(self):

        if not self.dataset_dir:
            return None

        folders = []

        for item in os.listdir(self.dataset_dir):

            path = os.path.join(
                self.dataset_dir,
                item
            )

            if os.path.isdir(path):

                if item.lower() != "sin_objeto":

                    folders.append(item)


        if len(folders) == 0:

            return None


        # Para nuestro proyecto inicialmente trabajaremos
        # con una sola clase.

        folders.sort()

        return folders[0]


    # ========================================================
    # OBTENER IMÁGENES
    # ========================================================

    def get_images(self, folder):

        extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        )

        images = []

        if not os.path.exists(folder):
            return images

        for filename in os.listdir(folder):

            if filename.lower().endswith(extensions):

                images.append(
                    os.path.join(
                        folder,
                        filename
                    )
                )

        return images


    # ========================================================
    # PREPARAR DATASET
    # ========================================================

    def prepare_dataset(self):

        if not self.dataset_dir:

            messagebox.showwarning(
                "Falta dataset",
                "Selecciona primero la carpeta dataset."
            )

            return


        if not self.labels_dir:

            messagebox.showwarning(
                "Faltan labels",
                "Selecciona primero la carpeta labels."
            )

            return


        self.class_name = self.detect_class()


        if not self.class_name:

            messagebox.showerror(
                "Error",
                "No se encontró ninguna clase de objeto."
            )

            return


        self.write_log("")
        self.write_log("=" * 70)
        self.write_log("INICIANDO PREPARACIÓN DEL DATASET")
        self.write_log("=" * 70)


        self.write_log(
            f"Clase detectada: {self.class_name}"
        )


        # ----------------------------------------------------
        # CARPETA DE SALIDA
        # ----------------------------------------------------

        parent = os.path.dirname(
            self.dataset_dir
        )

        self.output_dir = os.path.join(
            parent,
            "YOLO_DATASET"
        )


        # Si ya existe, preguntar

        if os.path.exists(self.output_dir):

            respuesta = messagebox.askyesno(
                "Dataset existente",
                "La carpeta YOLO_DATASET ya existe.\n\n"
                "¿Deseas eliminarla y crearla nuevamente?"
            )

            if not respuesta:
                return

            shutil.rmtree(
                self.output_dir
            )


        # ----------------------------------------------------
        # CREAR ESTRUCTURA
        # ----------------------------------------------------

        for split in [
            "train",
            "val",
            "test"
        ]:

            os.makedirs(
                os.path.join(
                    self.output_dir,
                    "images",
                    split
                )
            )

            os.makedirs(
                os.path.join(
                    self.output_dir,
                    "labels",
                    split
                )
            )


        # ----------------------------------------------------
        # IMÁGENES DEL OBJETO
        # ----------------------------------------------------

        object_folder = os.path.join(
            self.dataset_dir,
            self.class_name
        )


        object_images = self.get_images(
            object_folder
        )


        # ----------------------------------------------------
        # IMÁGENES SIN OBJETO
        # ----------------------------------------------------

        negative_folder = os.path.join(
            self.dataset_dir,
            "sin_objeto"
        )


        negative_images = self.get_images(
            negative_folder
        )


        self.write_log(
            f"Imágenes del objeto: {len(object_images)}"
        )

        self.write_log(
            f"Imágenes sin objeto: {len(negative_images)}"
        )


        # ----------------------------------------------------
        # MEZCLAR
        # ----------------------------------------------------

        random.seed(
            RANDOM_SEED
        )

        random.shuffle(
            object_images
        )

        random.shuffle(
            negative_images
        )


        # ----------------------------------------------------
        # DIVIDIR
        # ----------------------------------------------------

        object_train = int(
            len(object_images)
            * TRAIN_RATIO
        )

        object_val = int(
            len(object_images)
            * VAL_RATIO
        )


        object_train_images = object_images[
            :object_train
        ]

        object_val_images = object_images[
            object_train:
            object_train + object_val
        ]

        object_test_images = object_images[
            object_train + object_val:
        ]


        # Negativos

        negative_train = int(
            len(negative_images)
            * TRAIN_RATIO
        )

        negative_val = int(
            len(negative_images)
            * VAL_RATIO
        )


        negative_train_images = negative_images[
            :negative_train
        ]

        negative_val_images = negative_images[
            negative_train:
            negative_train + negative_val
        ]

        negative_test_images = negative_images[
            negative_train + negative_val:
        ]


        # ----------------------------------------------------
        # COPIAR
        # ----------------------------------------------------

        self.copy_images(
            object_train_images,
            "train",
            True
        )

        self.copy_images(
            object_val_images,
            "val",
            True
        )

        self.copy_images(
            object_test_images,
            "test",
            True
        )


        self.copy_images(
            negative_train_images,
            "train",
            False
        )

        self.copy_images(
            negative_val_images,
            "val",
            False
        )

        self.copy_images(
            negative_test_images,
            "test",
            False
        )


        # ----------------------------------------------------
        # CREAR DATA.YAML
        # ----------------------------------------------------

        self.create_yaml()


        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        self.write_log("")
        self.write_log("=" * 70)
        self.write_log("DATASET PREPARADO CORRECTAMENTE")
        self.write_log("=" * 70)

        self.write_log(
            f"📁 Ubicación:"
        )

        self.write_log(
            self.output_dir
        )

        self.write_log("")

        self.write_log(
            "TRAIN:"
        )

        self.write_log(
            f"  Objeto: {len(object_train_images)}"
        )

        self.write_log(
            f"  Sin objeto: {len(negative_train_images)}"
        )

        self.write_log("")

        self.write_log(
            "VALIDACIÓN:"
        )

        self.write_log(
            f"  Objeto: {len(object_val_images)}"
        )

        self.write_log(
            f"  Sin objeto: {len(negative_val_images)}"
        )

        self.write_log("")

        self.write_log(
            "TEST:"
        )

        self.write_log(
            f"  Objeto: {len(object_test_images)}"
        )

        self.write_log(
            f"  Sin objeto: {len(negative_test_images)}"
        )


        messagebox.showinfo(
            "Proceso terminado",
            "El dataset YOLO fue preparado correctamente.\n\n"
            f"Ubicación:\n{self.output_dir}"
        )


    # ========================================================
    # COPIAR IMÁGENES
    # ========================================================

    def copy_images(
        self,
        images,
        split,
        has_label
    ):

        for image_path in images:

            filename = os.path.basename(
                image_path
            )

            destination_image = os.path.join(
                self.output_dir,
                "images",
                split,
                filename
            )


            shutil.copy2(
                image_path,
                destination_image
            )


            # ------------------------------------------------
            # SOLO EL OBJETO TIENE LABEL
            # ------------------------------------------------

            if has_label:

                base = os.path.splitext(
                    filename
                )[0]

                source_label = os.path.join(
                    self.labels_dir,
                    base + ".txt"
                )


                if os.path.exists(
                    source_label
                ):

                    destination_label = os.path.join(
                        self.output_dir,
                        "labels",
                        split,
                        base + ".txt"
                    )

                    shutil.copy2(
                        source_label,
                        destination_label
                    )

                else:

                    self.write_log(
                        f"⚠ Falta label: {filename}"
                    )


    # ========================================================
    # CREAR DATA.YAML
    # ========================================================

    def create_yaml(self):

        yaml_path = os.path.join(self.output_dir,"data.yaml")

        # Obtener ruta absoluta del dataset
        dataset_path = os.path.abspath(self.output_dir)

        # Convertir \ de Windows a /
        dataset_path = dataset_path.replace("\\","/")

        with open(yaml_path,  "w",encoding="utf-8") as file:

            file.write(f"path: {dataset_path}\n")

            file.write("train: images/train\n")

            file.write("val: images/val\n")

            file.write("test: images/test\n")

            file.write("\n")

            file.write("names:\n")

            file.write(f"  0: {self.class_name}\n")


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = DatasetPreparator(
        root
    )

    root.mainloop()