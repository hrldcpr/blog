require 'open3'

Jekyll::Hooks.register :posts, :post_convert do |post|
  postprocess = post.data['postprocess']
  if postprocess
    new_content, status = Open3.capture2(postprocess, stdin_data: post.content)
    raise "#{postprocess} failed - #{status}" if not status.success?
    post.content = new_content
  end
end
