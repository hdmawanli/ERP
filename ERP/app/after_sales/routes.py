from flask import render_template, request, redirect, url_for, flash
from app import db
from app.after_sales import after_sales
from app.models import CustomerFeedback, TechnicalSupport, Customer, Product, User, SeedBatch
from app.after_sales.models import CustomerComplaint, ComplaintReply

# 客户反馈列表
@after_sales.route('/feedbacks/')
def feedback_list():
    feedbacks = CustomerFeedback.query.all()
    return render_template('after_sales/feedback_list.html', feedbacks=feedbacks)

# 添加客户反馈
@after_sales.route('/feedbacks/add/', methods=['GET', 'POST'])
def add_feedback():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id') or None
        feedback_type = request.form.get('feedback_type')
        content = request.form.get('content')

        new_feedback = CustomerFeedback(
            customer_id=customer_id,
            product_id=product_id,
            feedback_type=feedback_type,
            content=content
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash('客户反馈已成功添加', 'success')
        return redirect(url_for('after_sales.feedback_list'))

    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('after_sales/add_feedback.html', customers=customers, products=products)

# 编辑客户反馈
@after_sales.route('/feedbacks/edit/<int:feedback_id>', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    feedback = CustomerFeedback.query.get_or_404(feedback_id)
    if request.method == 'POST':
        feedback.customer_id = request.form.get('customer_id')
        feedback.product_id = request.form.get('product_id') or None
        feedback.feedback_type = request.form.get('feedback_type')
        feedback.content = request.form.get('content')
        feedback.status = request.form.get('status')
        feedback.solution = request.form.get('solution')
        feedback.solved_by = request.form.get('solved_by') or None

        if request.form.get('status') == '3' and not feedback.solve_time:
            from datetime import datetime
            feedback.solve_time = datetime.now()

        db.session.commit()
        flash('客户反馈已成功更新', 'success')
        return redirect(url_for('after_sales.feedback_list'))

    customers = Customer.query.all()
    products = Product.query.all()
    users = User.query.all()
    return render_template('after_sales/edit_feedback.html', feedback=feedback, customers=customers, products=products, users=users)

# 删除客户反馈
@after_sales.route('/feedbacks/delete/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = CustomerFeedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash('客户反馈已成功删除', 'success')
    return redirect(url_for('after_sales.feedback_list'))

# 技术支持列表
@after_sales.route('/supports/')
def support_list():
    supports = TechnicalSupport.query.all()
    return render_template('after_sales/support_list.html', supports=supports)

# 添加技术支持
@after_sales.route('/supports/add/', methods=['GET', 'POST'])
def add_support():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_id = request.form.get('product_id') or None
        support_type = request.form.get('support_type')
        title = request.form.get('title')
        content = request.form.get('content')

        new_support = TechnicalSupport(
            customer_id=customer_id,
            product_id=product_id,
            support_type=support_type,
            title=title,
            content=content
        )
        db.session.add(new_support)
        db.session.commit()
        flash('技术支持请求已成功添加', 'success')
        return redirect(url_for('after_sales.support_list'))

    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('after_sales/add_support.html', customers=customers, products=products)

# 编辑技术支持
@after_sales.route('/supports/edit/<int:support_id>', methods=['GET', 'POST'])
def edit_support(support_id):
    support = TechnicalSupport.query.get_or_404(support_id)
    if request.method == 'POST':
        support.customer_id = request.form.get('customer_id')
        support.product_id = request.form.get('product_id') or None
        support.support_type = request.form.get('support_type')
        support.title = request.form.get('title')
        support.content = request.form.get('content')
        support.status = request.form.get('status')
        support.assigned_to = request.form.get('assigned_to') or None
        support.solution = request.form.get('solution')

        if request.form.get('status') == '3' and not support.complete_time:
            from datetime import datetime
            support.complete_time = datetime.now()

        db.session.commit()
        flash('技术支持请求已成功更新', 'success')
        return redirect(url_for('after_sales.support_list'))

    customers = Customer.query.all()
    products = Product.query.all()
    users = User.query.all()
    return render_template('after_sales/edit_support.html', support=support, customers=customers, products=products, users=users)

# 删除技术支持
@after_sales.route('/supports/delete/<int:support_id>', methods=['POST'])
def delete_support(support_id):
    support = TechnicalSupport.query.get_or_404(support_id)
    db.session.delete(support)
    db.session.commit()
    flash('技术支持请求已成功删除', 'success')
    return redirect(url_for('after_sales.support_list'))

# 技术支持详情
@after_sales.route('/supports/<int:support_id>/')
def support_detail(support_id):
    support = TechnicalSupport.query.get_or_404(support_id)
    return render_template('after_sales/support_detail.html', support=support)

# 客户投诉列表
@after_sales.route('/complaints/')
def complaint_list():
    complaints = CustomerComplaint.query.all()
    return render_template('after_sales/complaint_list.html', complaints=complaints)

# 添加客户投诉
@after_sales.route('/complaints/add/', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        batch_id = request.form.get('batch_id')
        problem_description = request.form.get('problem_description')
        complaint_type = request.form.get('complaint_type') or None

        new_complaint = CustomerComplaint(
            customer_id=customer_id,
            batch_id=batch_id,
            problem_description=problem_description,
            complaint_type=complaint_type
        )
        db.session.add(new_complaint)
        db.session.commit()
        flash('客户投诉已成功添加', 'success')
        return redirect(url_for('after_sales.complaint_list'))

    customers = Customer.query.all()
    batches = SeedBatch.query.all()
    return render_template('after_sales/add_complaint.html', customers=customers, batches=batches)

# 编辑客户投诉
@after_sales.route('/complaints/edit/<int:complaint_id>', methods=['GET', 'POST'])
def edit_complaint(complaint_id):
    complaint = CustomerComplaint.query.get_or_404(complaint_id)
    if request.method == 'POST':
        complaint.customer_id = request.form.get('customer_id')
        complaint.batch_id = request.form.get('batch_id')
        complaint.problem_description = request.form.get('problem_description')
        complaint.complaint_type = request.form.get('complaint_type') or None
        complaint.status = int(request.form.get('status'))
        complaint.solution = request.form.get('solution') or None
        complaint.processed_by = request.form.get('processed_by') or None

        if complaint.status in [1, 2] and not complaint.processed_date:
            from datetime import datetime
            complaint.processed_date = datetime.now()

        db.session.commit()
        flash('客户投诉已成功更新', 'success')
        return redirect(url_for('after_sales.complaint_list'))

    customers = Customer.query.all()
    batches = SeedBatch.query.all()
    users = User.query.all()
    return render_template('after_sales/edit_complaint.html', complaint=complaint, customers=customers, batches=batches, users=users)

# 删除客户投诉
@after_sales.route('/complaints/delete/<int:complaint_id>', methods=['POST'])
def delete_complaint(complaint_id):
    complaint = CustomerComplaint.query.get_or_404(complaint_id)
    db.session.delete(complaint)
    db.session.commit()
    flash('客户投诉已成功删除', 'success')
    return redirect(url_for('after_sales.complaint_list'))

# 客户投诉详情
@after_sales.route('/complaints/<int:complaint_id>/')
def complaint_detail(complaint_id):
    complaint = CustomerComplaint.query.get_or_404(complaint_id)
    replies = ComplaintReply.query.filter_by(complaint_id=complaint_id).all()
    return render_template('after_sales/complaint_detail.html', complaint=complaint, replies=replies)

# 添加投诉回复
@after_sales.route('/complaints/<int:complaint_id>/reply/', methods=['POST'])
def add_complaint_reply(complaint_id):
    content = request.form.get('reply_content')
    user_id = request.form.get('user_id')  # 通常从登录用户获取

    new_reply = ComplaintReply(
        complaint_id=complaint_id,
        user_id=user_id,
        reply_content=content
    )
    db.session.add(new_reply)
    db.session.commit()
    flash('投诉回复已成功添加', 'success')
    return redirect(url_for('after_sales.complaint_detail', complaint_id=complaint_id))