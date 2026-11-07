import React from "react";
import { Button, Form } from "semantic-ui-react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { registerApi } from "../../api/user";

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: initialValues(),
    validationSchema: validationSchema(),
    onSubmit: async (formValues) => {
      try {
        await registerApi(formValues);
        toast.success("Cuenta creada. Ya puedes iniciar sesión.");
        navigate("/login");
      } catch (error) {
        toast.error(error.message);
      }
    },
  });

  const errorOf = (field) => formik.touched[field] && formik.errors[field];

  return (
    <div className="register-admin">
      <div className="register-admin__content">
        <h1>Registro</h1>

        <Form className="register-form-admin" onSubmit={formik.handleSubmit}>
          <label htmlFor="username">Username</label>
          <Form.Input
            id="username"
            name="username"
            placeholder="Username"
            autoComplete="username"
            value={formik.values.username}
            onChange={(e) => {
              formik.setFieldValue("username", e.target.value.replace(/\s+/g, ""));
            }}
            onBlur={formik.handleBlur}
            error={errorOf("username")}
          />
          <label htmlFor="email">Correo electrónico</label>
          <Form.Input
            id="email"
            name="email"
            placeholder="Correo electrónico"
            autoComplete="email"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={errorOf("email")}
          />
          <label htmlFor="password">Contraseña</label>
          <Form.Input
            id="password"
            name="password"
            type="password"
            placeholder="Contraseña"
            autoComplete="new-password"
            value={formik.values.password}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={errorOf("password")}
          />
          <label htmlFor="password_confirm">Confirmar contraseña</label>
          <Form.Input
            id="password_confirm"
            name="password_confirm"
            type="password"
            placeholder="Confirmar contraseña"
            autoComplete="new-password"
            value={formik.values.password_confirm}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={errorOf("password_confirm")}
          />
          <Button
            type="submit"
            content="Crear cuenta"
            primary
            fluid
            loading={formik.isSubmitting}
            disabled={formik.isSubmitting}
          />
        </Form>

        <p className="register-admin__link">
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link>
        </p>
      </div>
    </div>
  );
}

function initialValues() {
  return {
    username: "",
    email: "",
    password: "",
    password_confirm: "",
  };
}

function validationSchema() {
  return Yup.object({
    username: Yup.string()
      .required("El username es obligatorio")
      .matches(/^\S*$/, "El username no debe contener espacios"),
    email: Yup.string()
      .email("Correo electrónico no válido")
      .required("El correo electrónico es obligatorio"),
    password: Yup.string()
      .required("La contraseña es obligatoria")
      .min(8, "La contraseña debe tener al menos 8 caracteres")
      .matches(/[A-Z]/, "La contraseña debe contener al menos una letra mayúscula")
      .matches(/\d/, "La contraseña debe contener al menos un número")
      .matches(
        /[@$!%*?&#]/,
        "La contraseña debe contener al menos un carácter especial (@$!%*?&#)"
      ),
    password_confirm: Yup.string()
      .required("La confirmación de contraseña es obligatoria")
      .oneOf([Yup.ref("password")], "Las contraseñas no coinciden"),
  });
}
