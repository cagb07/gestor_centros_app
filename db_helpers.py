import pandas as pd
from database import get_db_connection


def get_all_submissions_with_details():
    conn = get_db_connection()
    df = pd.read_sql("""
        SELECT s.id, u.full_name as user_name, t.name as template_name, a.area_name, s.data, s.created_at,
               s.reviewed, s.reviewed_at, ru.full_name as reviewed_by_name
        FROM form_submissions s
        JOIN usuarios u ON s.user_id = u.id
        JOIN form_templates t ON s.template_id = t.id
        JOIN form_areas a ON t.area_id = a.id
        LEFT JOIN usuarios ru ON s.reviewed_by = ru.id
        ORDER BY s.created_at DESC
    """, conn)
    return df


def mark_submission_reviewed(submission_id, reviewer_user_id, reviewed=True):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if reviewed:
                cur.execute("UPDATE form_submissions SET reviewed = TRUE, reviewed_by = %s, reviewed_at = CURRENT_TIMESTAMP WHERE id = %s",
                            (reviewer_user_id, submission_id))
            else:
                cur.execute("UPDATE form_submissions SET reviewed = FALSE, reviewed_by = NULL, reviewed_at = NULL WHERE id = %s",
                            (submission_id,))
        conn.commit()
        return True, "Estado de revisión actualizado."
    except Exception as e:
        conn.rollback()
        return False, f"Error actualizando estado: {str(e)[:80]}"


def get_unreviewed_submissions():
    conn = get_db_connection()
    df = pd.read_sql("""
        SELECT s.id, u.full_name as user_name, t.name as template_name, a.area_name, s.data, s.created_at
        FROM form_submissions s
        JOIN usuarios u ON s.user_id = u.id
        JOIN form_templates t ON s.template_id = t.id
        JOIN form_areas a ON t.area_id = a.id
        WHERE s.reviewed = FALSE
        ORDER BY s.created_at DESC
    """, conn)
    return df


def update_area(area_id, area_name, description):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE form_areas SET area_name = %s, description = %s WHERE id = %s",
                        (area_name, description, area_id))
        conn.commit()
        return True, "Área actualizada."
    except Exception as e:
        conn.rollback()
        return False, f"Error actualizando área: {str(e)[:80]}"


def delete_area(area_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM form_areas WHERE id = %s", (area_id,))
        conn.commit()
        return True, "Área eliminada."
    except Exception as e:
        conn.rollback()
        return False, f"Error eliminando área: {str(e)[:80]}"


def get_user_by_id(user_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, username, role, full_name FROM usuarios WHERE id = %s", (user_id,))
        u = cur.fetchone()
    if u:
        return {"id": u[0], "username": u[1], "role": u[2], "full_name": u[3]}
    return None


def update_user(user_id, role=None, full_name=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if role is not None and full_name is not None:
                cur.execute("UPDATE usuarios SET role = %s, full_name = %s WHERE id = %s", (role, full_name, user_id))
            elif role is not None:
                cur.execute("UPDATE usuarios SET role = %s WHERE id = %s", (role, user_id))
            elif full_name is not None:
                cur.execute("UPDATE usuarios SET full_name = %s WHERE id = %s", (full_name, user_id))
        conn.commit()
        return True, "Usuario actualizado."
    except Exception as e:
        conn.rollback()
        return False, f"Error actualizando usuario: {str(e)[:80]}"


def delete_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        conn.commit()
        return True, "Usuario eliminado."
    except Exception as e:
        conn.rollback()
        return False, f"Error eliminando usuario: {str(e)[:80]}"
